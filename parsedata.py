import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# stop - route

dataset = {}

with open("api/stop-schedules.json","r") as fl:
    dataset = json.load(fl)

# output all routes for stops
outputdata = {}


directions = {}
days = {}
times = {}
stopnames = {}
routes = {}

for i in dataset:
    di = i[u'Direction']
    sn = i[u'Stop']
    rt = i[u'Route']
    ti = i[u'Time']
    day = i[u'Day']
    if di in directions:
        directions[di] += 1
    else:
        directions[di] = 1
    if sn in stopnames:
        stopnames[sn] += 1
    else:
        stopnames[sn] = 1
    if rt in routes:
        routes[rt] += 1
    else:
        routes[rt] = 1
    if ti in times:
        times[ti] += 1
    else:
        times[ti] = 1
    if sn in outputdata:
        if rt not in outputdata[sn]:
            outputdata[sn].append(rt)
    else:
        outputdata[sn] = []


#for i in directions:
#    print i,directions[i]
for i in outputdata:
    print outputdata[i]
#print routes[None]
#print len(stopnames)
#for i in stopnames:
#    print i.split("@")[0]
#print directions
#print times
#print stopnames
#print routes
