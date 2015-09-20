import json
import sys
import math
import geopy
import geopy.distance

reload(sys)
sys.setdefaultencoding("utf-8")

# stop - route

dataset = {}

with open("stop-locations.json","r") as fl:
    dataset = json.load(fl)

def getNearByBusStops(selfLocation, rangeInKm):
    location = selfLocation.split(",")
    selfLat = float(location[0])
    selfLong = float(location[1])
    nearByLocations = []

    pt1 = geopy.Point(selfLat, selfLong)

    for location in dataset:

        pt2 = geopy.Point(location["Latitude"], location["Longitude"])
        dist = geopy.distance.distance(pt1, pt2).km
        if(dist < rangeInKm):
            nearByLocations.append(location)

    return nearByLocations
