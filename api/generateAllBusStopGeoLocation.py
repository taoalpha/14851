import googlemaps
import json

gmaps = googlemaps.Client(key='AIzaSyA_xUmV_pXGdCYffUk1zTs9OaqnKCh2WSg')

locations = []
with open('datastops.txt') as f:
    line = f.readline()
    while line:
        searchString = str(line) + ',ithaca ny'
        stopLocation = gmaps.geocode(searchString)

        dictionary = {
            "Name":line,
            "Latitude":stopLocation[0]['geometry']['location']['lat'],
            "Longitude":stopLocation[0]['geometry']['location']['lng']
        }
        locations.append(dictionary)
        line = f.readline

with open('busStopLocations.json','w') as f:
    json.dump(locations, f)
    

