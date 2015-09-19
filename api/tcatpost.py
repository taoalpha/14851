import requests
import json
import bs4
import re
import get_stop_list
import getStopId


def getRouteInfo(startBusStop, endBusStop):
    form = getFormData(startBusStop, endBusStop)
    url ="http://tcat.nextinsight.com/index.php"

    html = requests.post(url,data=formdata).text

    soup = bs4.BeautifulSoup(html)

    allnames = soup.find_all('h4',class_="first")
    listsOfRoutes = []
    for i in allnames:
        option = i.get_text()
        estimated = i.find_next("p").get_text()
        description = str(i.find_next("p").find_next("p"))

        estimatedTime = re.search('.*: (.*)To.*',estimated).group(1)

        alltimes = re.findall('\d+:\d+ \w+',description)
        allstops = re.findall('stops/\d+">(.*?)\<\/a>',description)
        allroutes = re.findall('Route (\d+)',description)
        route = allroutes[0]
        if len(alltimes) == 2:
            print "no transfer needed"
            firstTransfer = 0
            secondTransfer = 0
        elif len(alltimes) == 3:
            print "3 times"
            firstTransferTime = alltimes[1]
            firstTransfer = allstops[1]
            firstTransferRoute = allroutes[1]
        elif len(alltimes) == 4:
            firstTransferTime = alltimes[1]
            firstTransfer = allstops[1]
            secondTransferTime = alltimes[2]
            secondTransfer = allstops[2]
            firstTransferRoute = allroutes[1]
        startTime = alltimes[0]
        endTime = alltimes[-1]
        startDestination = allstops[0]
        endDestination = allstops[-1]
        route = get_stop_list.get_stop_list(route,startTime.replace(' ',""),startDestination,endDestination,firstTransferRoute,firstTransfer,secondTransferTime.replace(' ',""))
        listsOfRoutes.append(route)
    return listsOfRoutes
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
