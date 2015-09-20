import tcatpost
import datetime

def get_info(startLocations, endLocations):
    bus_info = {}
    for startLocation in startLocations:
        for endLocation in endLocations:
            key = startLocation["Name"] + "|" + endLocation["Name"]
            bus_info[key] = {}

            routes, boardTimes, offTimes, routeNums, directionList =  tcatpost.getRouteInfo(startLocation["Name"], endLocation["Name"])

            print routes, boardTimes, offTimes, routeNums, directionList 

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

#get_info("42.44444","-72.58888")
