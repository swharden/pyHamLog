import urllib2
import os
import time
from zipfile import ZipFile
import sqlite3

dataFolder="./data/"
if not os.path.exists(dataFolder): os.makedirs(dataFolder)

def dl(link,saveIt=False):
    if saveIt==False: saveIt=link.split("/")[-1]
    print "downloading [%s] ..."%(saveIt)
    data = urllib2.urlopen(link)
    f=open(dataFolder+saveIt,'wb')
    f.write(data.read())
    f.close()
    print "complete!"
    if ".zip" in link:
        print "extracing..."
        ZipFile(dataFolder+saveIt).extractall(dataFolder)
        print "complete"
    return


def update_locations(downloadToo=False):
    if downloadToo:
        dl("http://www.country-files.com/n3fjp/arrlpre2.txt")

    f=open(dataFolder+"arrlpre2.txt")
    raw=f.readlines()
    f.close()

    mkit=""" create table locs (call text, country text, continent text,
        lat real, long real, star text, itu int, cq int);"""
    conn = sqlite3.connect(dataFolder+'db.sqlite')
    c = conn.cursor()
    c.execute("drop table if exists locs;")
    c.execute(mkit)
    for line in raw:
        line=line.replace(', '," - ").replace("'",'-')
        line=line.replace('"',"").replace('\n',"")
        if len(line)<10: continue
        call,cnt,con,lat,lo,star,itu,cq=line.split(",")
        query="INSERT INTO locs values('%s','%s','%s',%s,%s,'%s',%s,%s)"%(call,\
                cnt,con,float(lat),float(lo),star,int(itu),int(cq))
        c.execute(query)
    conn.commit()
    c.close()
    conn.close()
    print "LOADED",len(raw),"PREFIXES"

def update_addresses(downloadToo=False):
    if downloadToo:
        dl("http://wireless.fcc.gov/uls/data/complete/l_amat.zip")
        
    f=open(dataFolder+"EN.dat")
    raw=f.readlines()
    f.close()

    mkit="create table calldb"
    mkit+="(call text, name text, adr text, city text, state text, zip text);"
    conn = sqlite3.connect(dataFolder+'db.sqlite')
    c = conn.cursor()
    c.execute("drop table if exists calldb;")
    c.execute(mkit)
    
    for i in range(len(raw)):
        if i%10000==0:
            print "%d of %d (%.02f%%)"%(i,len(raw),i*100.0/len(raw))
        line=raw[i]
        if len(line)<10: continue
        line=line.replace("'",'-')
        line=line.split("|")
        query="INSERT INTO calldb values ('%s','%s','%s','%s','%s','%s')"%(line[4],line[7],line[15],line[16],line[17],line[18])
        c.execute(query)
    print "writing to file"
    conn.commit()
    c.close()
    conn.close()
    print "complete"
    print "LOADED",len(raw),"CALLSIGNS"

update_locations()
#update_addresses()

print("DONE")
time.sleep(1)
