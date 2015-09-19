import json

routeStopMap = {}

with open('route-schedules.json', 'r') as flr:
    dataset = json.load(flr)
    for dic in dataset:
        key = str(dic["Route"]) + "_" + str(dic["RouteInstance"]) + "_" + dic["Day"] + "_" + dic["Direction"]
        if key in routeStopMap:
            routeStopMap[key].append(str(dic["Stop"]))
        else:
            routeStopMap[key] = [dic["Stop"]]

with open('stop_lists.json', 'w') as flw:
    flw.write(json.dumps(routeStopMap))
