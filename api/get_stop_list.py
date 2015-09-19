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

def get_stop_list(route1, time1, stop1, end1, route2 = None, time2 = None, stop2 = None, end2 = None):
    result = helper(route1, time1, stop1, end1)
    if stop2 != None:
        result += helper(route2, time2, stop2, end2)
    return result

# print get_stop_list("92", "1:28PM", "East Hill Plaza", "Schwartz Performing Arts", "30", "1:50PM", "College @ Dryden", "Shops at Ithaca Mall @ Sears")
