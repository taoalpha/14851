import json

with open('route-schedules.json', 'r') as flr:
    dataset = json.load(flr)
    for dic in dataset:
        if dic["Route"] == 92 and dic["Day"] == "Saturday" and dic["Direction"] == "North":
            print str(dic["RouteInstance"]) + dic["Stop"] + dic["Time"] + dic["Direction"]
