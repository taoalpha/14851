import requests
import json
import bs4
import re
import get_stop_list

formdata = {
"start":"3540",
"end":"9028",
"day":6,
"starthours":1,
"startminutes":0,
"startampm":1,
"customer":1,
"sort":1,
"transfers":1,
"city":"Ithaca",
"radius":.25,
"search":"search"
}

url ="http://tcat.nextinsight.com/index.php"

html = requests.post(url,data=formdata).text

soup = bs4.BeautifulSoup(html)

allnames = soup.find_all('h4',class_="first")

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

    print "from:"+startDestination
    print "to:"+endDestination
    print "took route : " + route
    if firstTransfer:
        print "Get off from transfer at : " + firstTransfer +" at : "+ firstTransferTime
        print "tranfer to route : " + firstTransferRoute
    if secondTransfer:
        print "Board on transfer at : " + secondTransfer +" at : "+ secondTransferTime
    print "Next bus will arrive at: "+startTime
    print "Trip time: "+estimatedTime
    print "\n\n"
    print get_stop_list.get_stop_list(route,startTime.replace(' ',""),startDestination,endDestination,firstTransferRoute,firstTransfer,secondTransferTime.replace(' ',""))


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
