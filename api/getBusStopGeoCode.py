import json

busStopLocationDictionary = {}

def getBusStopGeoCode(busStopName):
    if len(busStopLocationDictionary) == 0 :
        loadBusStopLocations()
    return busStopLocationDictionary[busStopName]


def loadBusStopLocations():
    busStopLocationJson = []
    with open("busStopLocations.json","r") as f:
        busStopLocationJson = json.load(f)
    for data in busStopLocationJson:
        busStopLocationDictionary[data["Name"]] = (data["Latitude"], data["Longitude"])
