import json
import time
import getBusStopGeoCode
import os

os.chdir("/var/www/bigredtransit/templates/api")

routeStopMap = {}
with open('stop_lists_with_time.json', 'r') as sl:
    routeStopMap = json.load(sl)

dataset = {}
with open('route-schedules.json', 'r') as rs:
    dataset = json.load(rs)

def compare_time(time1, time2):
    fTime1 = time.strptime(time1, '%I:%M%p')
    fTime2 = time.strptime(time2, '%I:%M%p')
    return fTime1 < fTime2

def helper(route, begin, end, beginTime, endTime, day):
    ifEndExists = True
    ifBeginExists = True
    beginIndex = 0
    endIndex = 0
    result = []

    for dic in dataset:
        if route == str(dic["Route"]) and begin == dic["Stop"] and beginTime == dic["Time"]:
            key = str(route) + "_" + str(dic["RouteInstance"])
            stopList = routeStopMap[key]

            stopNameList = []
            stopTimeList = []

            for stop in stopList:
                stopNameList.append(stop.split(",")[0])
                stopTimeList.append(stop.split(",")[1])

            if begin in stopNameList:
                beginIndex = stopNameList.index(begin)
            else:
                ifBeginExists = False
                for index, time in enumerate(stopTimeList):
                    if compare_time(time, beginTime):
                        beginIndex = index
                        break

            if end in stopNameList:
                endIndex = stopList.index(end)
            else:
                ifEndExists = False
                for index, time in enumerate(reversed(stopTimeList)):
                    if compare_time(endTime, time):
                        endIndex = len(stopTimeList) - 1 - index
                        break

            result = stopNameList[beginIndex : endIndex+1]
            if ifBeginExists:
                result.insert(0, begin)
            if ifEndExists:
                result.append(end)
            return result, dic["Directions"]


def get_stop_list(route1, stop1Name, stop1Time, end1Name, end1Time, day1, route2 = None, stop2Name = None, stop2Time = None, end2Name = None, end2Time = None, day2 = None):

    directionList = []
    result, d1  = helper(route1, stop1Name, end1Name, stop1Time, end1Time, day1)
    directionList.append(d1)

    if stop2Name != None:
        r, d2 = helper(route2, stop2Name, end2Name, stop2Time, end2Time, day2)
        result += r
        directionList.append(d2)

    geoResult = []
    for stop in result:
        geoResult.append(getBusStopGeoCode.getBusStopGeoCode(stop))

    return geoResult, directionList

# print get_stop_list("92", "Hasbrouck Apts.", "3:00PM", "Sage Hall", "3:16PM", "Saturday")
