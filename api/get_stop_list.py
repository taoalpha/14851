import json
import time

routeStopMap = {}
with open('stop_lists.json', 'r') as sl:
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
    for dic in dataset:
        if route == str(dic["Route"]) and begin == dic["Stop"] and beginTime == dic["Time"] and day == dic["Day"]:
            key = str(route) + "_" + str(dic["RouteInstance"]) + "_" + dic["Day"]
            print key
            stopList = routeStopMap[key]
            stopNameList = []
            stopTimeList = []
            for stop in stopList:
                stopNameList.append(stop.split("?")[0])
                stopTimeList.append(stop.split("?")[1])
            beginIndex = stopNameList.index(begin)
            if end in stopNameList:
                endIndex = stopList.index(end)
            else:
                ifEndExists = False
                endIndex = len(stopTimeList) - 1
                for index, time in enumerate(reversed(stopTimeList)):
                    if compare_time(endTime, time):
                        endIndex -= index
                        break;

            return (stopList[beginIndex : endIndex+1], ifEndExists)

def get_stop_list(route1, stop1Name, stop1Time, end1Name, end1Time, day1, route2 = None, stop2Name = None, stop2Time = None, end2Name = None, end2Time = None, day2 = None):
    result, ifEndExists = helper(route1, stop1Name, end1Name, stop1Time, end1Time, day1)
    if not ifEndExists:
        result.append(end1Name)
    if stop2Name != None:
        routingList, ifEndExists = helper(route2, stop2Name, end2Name, stop2Time, end2Time, day2)
        result += routingList
        if not ifEndExists:
            result.append(end2Name)
    return result

# print get_stop_list("92", "East Hill Plaza", "3:28PM", "Sage Hall", "3:39PM", "Saturday")
