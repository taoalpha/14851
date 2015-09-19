import requests
import json
import bs4
import re

formdata = {
"start":"3540",
"end":"9028",
"day":6,
"starthours":1,
"startminutes":0,
"startampm":1,
"customer":1,
"sort":1,
"transfers":2,
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
    if len(alltimes) == 2:
        print "no transfer needed"
    elif len(alltimes) == 3:
        firstTransferTime = alltimes[2]
        firstTransfer = allstops[2]
    elif len(alltimes) == 4:
        firstTransferTime = alltimes[2]
        firstTransfer = allstops[2]
        secondTransferTime = alltimes[3]
        secondTransfer = allstops[3]
    startTime = alltimes[0]
    endTime = alltimes[-1]
    startDestination = allstops[0]
    endDestination = allstops[-1]

    print "from:"+startDestination
    print "to:"+endDestination
    if firstTransfer:
        print "first transfer at : " + firstTransfer +" at : "+ firstTransferTime
    if secondTransfer:
        print "second transfer at : " + secondTransfer +" at : "+ secondTransferTime

    print "Next bus at: "+startTime
    print "Trip time: "+estimatedTime
    print "\n\n"

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
