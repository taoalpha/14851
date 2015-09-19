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

def route_stop_list(route1, time1, begin, end, route2 = None, stop2=None, time2 = None, route3 = None, stop3=None, time3 = None):
    result = []
    if stop2 != None:
        result += helper(route1, time1, begin, stop2)
        if stop3 != None:
            result += helper(route2, time2, stop2, stop3)
            result += helper(route3, time3, stop3, end)
        else:
            result += helper(route2, time2, stop2, end)
    else:
        result = result + helper(route1, time1, begin, end)
    return result

# print route_stop_list("74", "7:30AM", "Shops at Ithaca Mall @ Sears", "Groton Express Mart")
