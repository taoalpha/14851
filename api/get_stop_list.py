import json

routeStopMap = {}
with open('stop_lists.json', 'r') as sl:
    routeStopMap = json.load(sl)

dataset = {}
with open('route-schedules.json', 'r') as rs:
    dataset = json.load(rs)

def helper(route, time, begin, end):
    for dic in dataset:
        if route == str(dic["Route"]) and begin == dic["Stop"] and time == dic["Time"]:
            key = str(route) + "_" + str(dic["RouteInstance"]) + "_" + dic["Day"] + "_" + dic["Direction"]
            stopLists = routeStopMap[key]
            beginIndex = stopLists.index(begin)
            endIndex = stopLists.index(end)
            return stopLists[beginIndex : endIndex+1]

def route_stop_list(route, time, begin, end, stop1=None, time1 = None, stop2=None, time2 = None):
    result = []
    if stop1 != None:
        result += helper(route, time, begin, stop1)
        if stop2 != None:
            result += helper(route, time1, stop1, stop2)
            result += helper(route, time2, stop2, end)
        else:
            result += helper(route, time1, stop1, end)
    else:
        result = result + helper(route, time, begin, end)
    return result

# print route_stop_list("74", "7:30AM", "Shops at Ithaca Mall @ Sears", "Groton Express Mart")
