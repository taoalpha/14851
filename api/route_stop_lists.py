import json

routeStopMapWithTime = {}
routeStopMap = {}

with open('route-schedules.json', 'r') as flr:
    dataset = json.load(flr)
    for dic in dataset:
        key = str(dic["Route"]) + "_" + str(dic["RouteInstance"])
        if key in routeStopMap:
            routeStopMapWithTime[key].append(dic["Stop"] + "," + dic["Time"])
            routeStopMap[key].append(dic["Stop"])
        else:
            routeStopMapWithTime[key] = [dic["Stop"] + "," + dic["Time"]]
            routeStopMap[key] = [dic["Stop"]]

with open('stop_lists_with_time.json', 'w') as flw:
    flw.write(json.dumps(routeStopMapWithTime))

with open('stop_lists.json', 'w') as f:
    f.write(json.dumps(routeStopMap))
