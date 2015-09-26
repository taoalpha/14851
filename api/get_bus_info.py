import tcatpost
import datetime

def get_info(startLocations, endLocations):
    bus_info = {}
    for startLocation in startLocations:
        for endLocation in endLocations:
            key = startLocation[0]["Name"] + "|" + endLocation[0]["Name"]
            bus_info[key] = {}

            routes, boardTimes, offTimes, directionList =  tcatpost.getRouteInfo(startLocation[0]["Name"], endLocation[0]["Name"])

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

    myDic = {}
    for route, info in bus_info.iteritems():
        if len(info["Routes"]) != 0:
            if not "Routes" in myDic:
                myDic["Routes:"] = info["Routes"]
            else:
                myDic["Routes:"] += info["Routes"]
            if not "Direction" in myDic:
                myDic["Direction"] = info["Direction"]
            else:
                myDic["Direction"] += info["Direction"]
            if not "Time" in myDic:
                myDic["Time"] = info["Time"]
            else:
                myDic["Time"] += info["Time"]

    #print bus_info
    #print "bus_info"
    #print bus_info
    return myDic
