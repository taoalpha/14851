import googlemaps
import json
import time

#gmaps = googlemaps.Client(key='AIzaSyA_xUmV_pXGdCYffUk1zTs9OaqnKCh2WSg')
gmaps = googlemaps.Client(key='AIzaSyDuzxDlvLheX4jDcuLJfQWG7LCrPXG6fyQ')

locations = []
with open('datastops.txt') as f:
    lines = f.readlines()
    for line in lines:
        time.sleep(1)
        searchString = line + ',ithaca ny'
        stopLocation = gmaps.geocode(searchString)
        lat = 0.0
        lng = 0.0
        if stopLocation is not None and len(stopLocation) != 0:
            lat = stopLocation[0]['geometry']['location']['lat']
            lng = stopLocation[0]['geometry']['location']['lng']

        dictionary = {
            "Name":line,
            "Latitude":lat,
            "Longitude":lng
        }
        print dictionary
        locations.append(dictionary)


with open('busStopLocations.json','w') as f:
    json.dump(locations, f)
    

