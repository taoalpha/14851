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
    a = None, 0;
    b = None, 0;
    c = None, 0;
    for location in dataset:
        pt2 = geopy.Point(location["Latitude"], location["Longitude"])
        dist = geopy.distance.distance(pt1, pt2).km
        if(c[1] == 0):
            c = location, dist
        elif(b[1] == 0):
            b = location, dist
        elif(a[1] == 0):
            a = location, dist        
            array = [a, b ,c]
            array.sort(key=lambda x: x[1])
            a = array[0]
            b = array[1]
            c = array[2]
        elif(dist < rangeInKm):
            furthest = max(max(a[1],b[1]),c[1]) 
            if(dist < furthest):
                c = location, dist
                array = [a, b ,c]
                array.sort(key=lambda x: x[1])
                a = array[0]
                b = array[1]
                c = array[2]
    toReturn = []
    if(a[0] != None):
        toReturn.append(a)
    if(b[0] != None):
        toReturn.append(b)
    if(c[0] != None):
        toReturn.append(c)
    return toReturn