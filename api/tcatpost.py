import sys
sys.path.append('./')
import requests
import json
import bs4
import re
import get_stop_list
import getStopId
import datetime
import time

def getRouteInfo(startBusStop, endBusStop):
    form = getFormData(startBusStop, endBusStop)
    url ="http://tcat.nextinsight.com/index.php"

    html = requests.post(url,data=form).text

    soup = bs4.BeautifulSoup(html)

    allnames = soup.find_all('h4',class_="first")
    print len(allnames)
    listsOfRoutes = []
    listOfStartTimes = []
    listOfEndTimes = []
    listOfRouteNums = []
    directionList = []
	
    for i in allnames:
        # option = i.get_text()
        # estimated = i.find_next("p").get_text()
        description = str(i.find_next("p").find_next("p"))

        # estimatedTime = re.search('.*: (.*)To.*',estimated).group(1)

        alltimes = re.findall('\d+:\d+ \w+',description)
        allstops = re.findall('stops/\d+">(.*?)\<\/a>',description)
        allroutes = re.findall('Route (\d+)',description)

        route1 = allroutes[0]
        stop1name = allstops[0]
        stop1time = alltimes[0]
        end1name = allstops[1]
        end1time = alltimes[1]
        day1 = datetime.datetime.today()

        route2 = None
        stop2name = None
        stop2time = None
        end2name = None
        end2time = None
        day2 = None

        if len(alltimes) == 4:
            route = allroutes[1]
            stop2name = allstops[2]
            stop2time = alltimes[2]
            end2name = allstops[3]
            end2time = alltimes[3]
            day2 = datetime.datetime.today()

        (route, directionList) = get_stop_list.get_stop_list(route1, stop1name, stop1time, end1name, end1time, day1, route2, stop2name, stop2time, end2name, end2time, day2)
	print route
        listsOfRoutes.append(route)
        listOfStartTimes.append(stop1time)
        if len(alltimes) == 4:
            listOfEndTimes.append(end2time)
        else:
            listOfEndTimes.append(end1time)
        listOfRouteNums.append(allroutes)

    return listsOfRoutes, listOfStartTimes, listOfEndTimes, listOfRouteNums, directionList
    # print "from:"+startDestination
    # print "to:"+endDestination
    # print "took route : " + route
    # if firstTransfer:
    #     print "Get off from transfer at : " + firstTransfer +" at : "+ firstTransferTime
    #     print "tranfer to route : " + firstTransferRoute
    # if secondTransfer:
    #     print "Board on transfer at : " + secondTransfer +" at : "+ secondTransferTime
    # print "Next bus will arrive at: "+startTime
    # print "Trip time: "+estimatedTime
    # print "\n\n"
    # #print get_stop_list.get_stop_list(route,startTime.replace(' ',""),startDestination,endDestination,firstTransferRoute,firstTransfer,secondTransferTime.replace(' ',""))

def getDayRepNumber(day):
    return {
        'Sun': 0,
        'Mon': 1,
        'Tue': 2,
        'Wed': 3,
        'Thu': 4,
        'Fri': 5,
        'Sat': 6
    }.get(day)

def getFormData(start, end):

    startID = getStopId.getStopId(start)
    print startID
    endId = getStopId.getStopId(end)

    day = getDayRepNumber(time.strftime("%a"))
    starthours = time.strftime("%I")
    startminutes = time.strftime("%M")
    startampm = 0 if time.strftime("%p") == "AM" else 1

    formdata = {
        "start":startID,
        "end":endId,
        "day":day,
        "starthours":starthours,
        "startminutes":startminutes,
        "startampm":startampm,
        "customer":1,
        "sort":1,
        "transfers":0,
        "city":"Ithaca",
        "radius":.25,
        "search":"search"
    }

    return formdata


#allidurl = "http://tcat.nextinsight.com/allstops.php"
#allid_html = requests.post(allidurl,data=formdata).text
#allid_soup = bs4.BeautifulSoup(allid_html)
#
#allids = {}
#areaids = allid_soup.find('div',id='leftColSub').find_all('a')
#for i in areaids:
#    stopid = re.search('^/.*/(.*)',i.attrs["href"]).group(1)
#    stopname = i.get_text()
#    allids[stopname] = stopid

#print allids
