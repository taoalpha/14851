import tcatpost
import datetime

def get_info(startLocations, endLocations):
    bus_info = {}
    for startLocation in startLocations:
        for endLocation in endLocations:
            key = startLocation["Name"] + "|" + endLocation["Name"]
            bus_info[key] = {}

            routes, boardTimes, offTimes, directionList =  tcatpost.getRouteInfo(startLocation["Name"], endLocation["Name"])

            #bus_info[key]["RouteNums"] = routeNums
            bus_info[key]["Key"] = key
            bus_info[key]["Routes"] = routes

            bus_info[key]["Time"] = []
            #bus_info[key]["Direction"] = directionList
            bus_info[key]["Direction"] = key.split("|")[0]+"-"+key.split("|")[1]

            for t in range(len(boardTimes)):
                bt = datetime.datetime.strptime(boardTimes[t], '%I:%M %p')
                if datetime.datetime.now() - bt < datetime.timedelta(0, 600):
                    bus_info[key]["Time"].append("<strong>" + t + "</strong>")
                else:
                    bus_info[key]["Time"].append(boardTimes[t] + " - " + offTimes[t])

    result = []
    for route, info in bus_info.iteritems():
        if len(info["Routes"]) != 0:
            result.append(info)
    #print bus_info
    #print "bus_info"
    #print bus_info
    return result

get_info([{"Latitude": 42.4447409, "Name": "Carpenter Hall", "Longitude": -76.4841488}, {
    "Latitude": 42.4472546,
    "Name": "Uris Hall",
    "Longitude": -76.48225029999999
  }], [{"Latitude": 42.4365165, "Name": "East Hill Plaza", "Longitude": -76.46263259999999}])
