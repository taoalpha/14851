import json

def getBusStopGeoCode(busStopName):
    stopLocations = loadBusStopLocations
    return stopLocations(busStopName)

def loadBusStopLocations():
    locations = {}
    with open("busStopLocations.json","r") as f:
        dataset = json.load(f)
    for data in dataset:
        locations[data["Name"]] = (data["Latitude"], data["Longitude"])
    return locations