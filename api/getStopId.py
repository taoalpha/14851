import json


busStopIdDictionary = {}
def getStopId(name):
    if len(busStopIdDictionary) == 0:
        loadBusStopIdDictionary()
    if name in busStopIdDictionary:
        return busStopIdDictionary[name]
    else:
        return 0


def loadBusStopIdDictionary():
    with open("allids.json","r") as f:
        busStopLocationIDJson = json.load(f)

