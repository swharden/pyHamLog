import urllib

username='aj4vd'
password='oogabooga'
session=''

def stripChars(s,chars="<>/"):
    for char in chars:
        s=s.replace(char,"")
    return s

def xmlGetBlock(data,key):
    if not key in data:
        return False
    data=data.split('<'+key+'>')[1]
    data=data.split('</'+key+'>')[0]
    return data

def xmlToDict(data):
    
    d={}
    data=data.replace('\t','')
    data=data.split("\n")
    for line in data:
        if not "</" in line: continue
        line=line.split("</")[0]
        line=line.replace("<","")
        key,val=line.split(">")
        d[key]=val
    #for key in d.keys(): print key,d[key]
    print "looked up %s"%(d['callsign'])
    return d

def newSession():
    global session, username, password
    if len(username)<3: username=raw_input("HamQTH login:")
    if len(password)<3: password=raw_input("HamQTH password:")
    print "logging in with:",username,"*"*len(password)
    url='http://www.hamqth.com/xml.php?u=%s&p=%s'%(username,password)
    data=urllib.urlopen(url).read()
    if "error" in data:
        print "ERROR!"
        print data
        raw_input("now what?")
    else:
        data=stripChars(data)
        session=data.split("session_id")[1]
        print "SESSION:",session                                         
    return session

def lookup(call):
    while session=='': newSession()
    url='http://www.hamqth.com/xml.php?'
    url+='id=%s&callsign=%s&prg=pyCallLookup_V1'%(session,call)
    data=urllib.urlopen(url).read()
    data=xmlGetBlock(data,'search')
    if data==False: return False
    return xmlToDict(data)

def genHtmlFor(call):
    d=lookup(call)
    out="<html><body>"
    if d==False:
        out+="NOT FOUND:<br>"+call
        out+="</body></html>"
        return out
    out+="<table>\n"
    out+='<tr><td colspan="2" align="center"><b>%s</b></td></tr>\n'%d['callsign'].upper()
    for f in ['adr_name','adr_city','us_state','adr_country']:
        if not f in d.keys(): continue
        out+='<tr><td align="right">%s:</td><td>%s</td></tr>\n'%(f.replace("_"," "),d[f])
    out+="</table>"
    out+="</body></html>"
    return out
