## Created 2012 by Scott Harden, AJ4VD
## Updated October 19, 2014 by Andrew Milluzzi, KK4LWR

## Edits:
## - Updated logging date

## Instructions: Update to start of Contest. See instructions on around line 130.

import sqlite3
import time
import pylab
import numpy
import datetime

def toListie(t):
    for i in range(len(t)):
        t[i]=t[i][0]
    return t

class dbStat():
    
    def __init__(self):
        self.con=sqlite3.connect('scr.db')
        self.c=self.con.cursor()
        self.table='qsos'

    def getOpData(self):
        ops=toListie(self.runQuery("SELECT DISTINCT operator FROM qsos"))
        opData={}
        for op in ops:
            timePoints=toListie(self.runQuery("SELECT stamp FROM qsos WHERE operator='%s'"%op))
            for i in range(len(timePoints)):
                timePoints[i]=time.mktime(time.strptime(timePoints[i], "%Y-%m-%d %H:%M:%S"))
            #print op,len(timePoints),timePoints[1]
            opData[op]=timePoints
            #print op,"had",len(timePoints),"contacts"
        return opData
    
    def runQuery(self,query,commit=False):
        if not "SELECT" in query:
            f=open('log.txt','a')
            f.write("%.02f %s\n"%(time.time(),query.replace("\n"," ")))
            f.close()
            print "RUNNING QUERY:"
            print query
        query=query.upper()
        data=list(self.c.execute(query).fetchall())
        if commit==True: self.commit()
        return data
           
    def disconnect(self):
        self.con.close()

def kernGauss(size):
    size=float(size)
    gaussian = lambda x: numpy.exp(-x**2/size)
    g = gaussian(numpy.arange(-size/2,size/2))
    return g / g.sum()

d=dbStat()
opData=d.getOpData()



##############################
##############################
##############################

opNames=[]
opHours=[]
opRates=[]
opTotls=[]
totalHours=0
for op in opData.keys():
    ssis=[]
    for i in range(len(opData[op])-1):
        ssi=(opData[op][i+1]-opData[op][i])/60.0
        if ssi>15:continue
        ssis.append(ssi)
    opNames.append(op)
    opHours.append(sum(ssis)/60.0)
    totalHours += sum(ssis)/60.0
    opRates.append(len(ssis)*60.0/sum(ssis))
    opTotls.append(len(opData[op]))
    print "%s operated %.02f hr averaging %.02f QSOs/hr"%\
            (op,sum(ssis)/60.0,len(ssis)*60.0/sum(ssis))


#print totalHours
			
pylab.figure()
pylab.title("Contacts Made")
pylab.ylabel("total number of contacts")
pylab.xlabel("Operator")
pylab.bar(numpy.arange(len(opNames))-.4,opTotls,fc='g')
pylab.xticks(numpy.arange(len(opNames)),opNames)
pylab.savefig('./pages/totals.png')
pylab.clf()

#raise SystemExit(1)

pylab.figure()
pylab.title("QSO Rate")
pylab.ylabel("average contacts per hour")
pylab.xlabel("Operator")
pylab.bar(numpy.arange(len(opNames))-.4,opRates,fc='r')
pylab.xticks(numpy.arange(len(opNames)),opNames)
pylab.savefig('./pages/rate.png')
pylab.clf()


pylab.figure()
hoursLabel = "Operating Time - Total Hours: %.02f" % totalHours
pylab.title(hoursLabel)
pylab.ylabel("Cumulative Hours")

pylab.xlabel("Operator")
pylab.bar(numpy.arange(len(opNames))-.4,opHours,fc='b')
pylab.xticks(numpy.arange(len(opNames)),opNames)
pylab.savefig('./pages/optime.png')
pylab.clf()



#kernel=[1.0/3600]*3600
kernel=kernGauss(120)
dySec=60*60*24
divider=15

# UPDATE THIS LINE BY TIME OF NEW EVENT
# epoch seconds of first day of event
startEpoch = time.mktime(time.strptime("10/20/2014", "%m/%d/%Y"))
startEpoch=startEpoch+(60*60*8)
contestLen=5.5*(60*60*24) #5 days
endEpoch=startEpoch+contestLen
timePoints=numpy.arange(startEpoch,endEpoch,divider)


for op in opData.keys():
    hist, bin_edges = numpy.histogram([opData[op]], bins=timePoints)
    print "processing data for",op
    spikeTimes=opData[op]
    spikeTimePoints=numpy.digitize(spikeTimes,timePoints)
    digitalValues=numpy.zeros(len(timePoints))
    digitalValues[spikeTimePoints]=1
    smooth=numpy.convolve(digitalValues,kernel)*60*60/divider
    newTimes=numpy.arange(startEpoch,endEpoch+divider*len(smooth),divider)
    #newTimes=newTimes+60*60*4
    newTimes=map(datetime.datetime.fromtimestamp, newTimes)
    #pylab.plot(newTimes,smooth,label=op)
    opData[op]=smooth


for day in range(5):
    print "plotting day",day+1
    #figs.append(pylab.figure())
    fig=pylab.figure(figsize=(10,5))
    i1=(4*60*60+dySec*(day))/divider
    i2=i1+dySec/divider
    #cut it in half to only show 12 hours
    #i1=i1+dySec/2/divider
    dayTimes=newTimes[i1:i2]
    for op in opData.keys():
        daySmooth=opData[op][i1:i2]
        if len(dayTimes)!=len(daySmooth): continue
        pylab.plot(dayTimes,daySmooth,label=op,lw=2)
    pylab.ylabel("Contact Rate (QSOs per hour)")
    pylab.title("Day %d"%(day+1))
    pylab.grid()
    fig.autofmt_xdate()
    pylab.legend(loc=1)
    pylab.axis([None,None,None,120])
    pylab.savefig("./pages/day"+str(day)+".png")
    #pylab.close()
    pylab.clf()

print "plotting the week"
fig=pylab.figure(figsize=(10,5))
for op in opData.keys():
	#print len(opData[op])
	#print len(newTimes)
	if len(opData[op]) > len(newTimes): continue
	pylab.plot(newTimes[0:len(opData[op])],opData[op],label=op)
	
pylab.ylabel("Contact Rate (QSOs per hour)")
pylab.title("All Week")
pylab.grid()
fig.autofmt_xdate()
pylab.legend(loc=1)
pylab.axis([None,None,None,120])
pylab.savefig("./pages/dayAll.png")
#pylab.close()
pylab.clf()

print "DONE"









