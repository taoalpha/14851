import json


busStopIdDictionary = {}
def getStopId(name):
    global busStopIdDictionary

    if len(busStopIdDictionary) == 0:
        loadBusStopIdDictionary()
    if name in busStopIdDictionary:
        return busStopIdDictionary[name]
    else:
        return 0


def loadBusStopIdDictionary():
    global busStopIdDictionary
    with open("allids.json","r") as f:
        busStopIdDictionary = json.load(f)

