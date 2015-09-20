import json

count = {}
with open('route-schedules.json', 'r') as flr:
    dataset = json.load(flr)
    for dic in dataset:
        if dic["Day"] in count:
            count[dic["Day"]] += 1
        else:
            count[dic["Day"]] = 1

print count
