import json


busStopIdDictionary = {}
def getStopId(name):
    if len(busStopIdDictionary) == 0:
        loadBusStopIdDictionary()
    return busStopIdDictionary[name]


def loadBusStopIdDictionary():
    with open("allids.json","r") as f:
        busStopLocationIDJson = json.load(f)

