import tcatpost
import datetime

def get_info(startLocations, endLocations):
    bus_info = {}
    for startLocation in startLocations:
        for endLocation in endLocations:
            key = startLocation["Name"] + "|" + endLocation["Name"]
            bus_info[key] = {}

            routes, boardTimes, offTimes, routeNums, directionList =  tcatpost.getRouteInfo(startLocation["Name"], endLocation["Name"])

            bus_info[key]["RouteNums"] = routeNums
            bus_info[key]["Routes"] = routes

            bus_info[key]["Time"] = []
            bus_info[key]["Direction"] = directionList

            for t in range(len(boardTimes)):
                bt = datetime.datetime.strptime(boardTimes[t], '%I:%M %p')
                if datetime.datetime.now() - bt < datetime.timedelta(0, 600):
                    bus_info[key]["Time"].append("<strong>" + t + "</strong>")
                else:
                    bus_info[key]["Time"].append(boardTimes[t] + " - " + offTimes[t])

    return bus_info

get_info([{"Latitude": 42.4447409, "Name": "Carpenter Hall", "Longitude": -76.4841488
}], [{"Latitude": 42.4365165, "Name": "East Hill Plaza", "Longitude": -76.46263259999999}])
