import datetime
from database import *

pageFolder='./pages/'
colNames=['id','stamp','call','freq','mode',\
          'sent','got','qth','class','operator','notes']

def local_to_utc(t):
    secs = time.mktime(t)
    return time.gmtime(secs)

def results2editable(lines):
    out=""
    header,data=lines
    data=list(data)
    out+='<form name="input" action="act-edit-%s" method="post">'%data[0]
    out+='<div align="center">'
    out+="<h2>EDIT ENTRY #%s</h2>"%data[0]
    out+='<table cellpadding="5" cellspacing="5">'
    for i in range(len(header)):
        if data[i]==None: data[i]=''
        out+='<tr><td align="right">%s</td>'%(header[i])
        out+='<td align="left">'
        dis=""
        if i==0:
            dis='readonly="readonly"'
        out+='<input type="text" %s id="%s" name="%s" value="%s"><br>'%(dis,colNames[i],colNames[i],data[i])
        out+="</td></tr>"
    out+="</table>"
    out+='<input type="submit" name="action" value="MODIFY THIS CONTACT">'
    out+="</div>"
    out+="</form>"
    return out

def results2html(lines,header=None,editable=True):
    if "ID" in lines[0] or header==True:rowid=-1
    else:rowid=1
    sp="     "
    out='\n\n<table border="0" cellpadding="5" cellspacing="0">\n'
    for line in lines:
        rowid+=1
        if rowid>2: rowid=1
        out+=sp+'<tr class="row%d">\n'%(rowid)
        #for item in line:
        for i in range(1,len(line)):
            item=line[i]
            if i in [2,9] and rowid>0:
                item='<a href="http://www.qrz.com/db/%s">%s</a>'%(item,item)
            if item==None: item="<!--None-->"
            out+=sp*2+"<td>%s</td>\n"%item
        if editable==True:
            if rowid==0:
                out+=sp*2+"<td></td>\n"
                out+=sp*2+"<td></td>\n"                
            else:
                edit="act-edit-%d"%line[0]
                delete="act-delete-%d"%line[0]
                out+=sp*2+'<td><a href="%s">edit</a></td>\n'%edit
                out+=sp*2+'<td><a href="%s">delete</a></td>\n'%delete
        out+=sp+"</tr>\n"
    out+="</table>\n\n"
    return out

def stats2html(stats):
    scoreC=stats["score"]

    scoreC=format(scoreC, ",d")   # 1,234
    #print "{:,d}".format(1234) # 1,234

    out="<h2>SCORE: %s</h2>"%scoreC
    
    out+="<b>QSO Points: %d</b><br>"%stats["qsopoints"]
    out+="%d total QSOs<br>"%stats["qsos"]
    out+="%d SSB (%d points)<br>"%(stats["phone"],stats["phone"])
    out+="%d digital (%d points)<br><br>"%(stats["dig"],stats["dig"]*2)
    
    out+="<b>Multiplier: %d</b><br>"%stats["mult"]
    out+="%d locations (%d)<br>"%(stats["locations"],stats["locations"])
    out+="%d clubs (%d)<br>"%(stats["clubs"],stats["clubs"]*2)
    out+="%d schools (%d)<br>"%(stats["schools"],stats["schools"]*5)

    locs='<br><br><br>'
    for loc in stats["loclist"]:
        locs+="%s, "%(loc)
    locs=locs[:-2]
    out+='<span style="font-size:10px;color:#CCCCCC;">'
    out+='locations: <i>%s</i></span><br>'%(locs)

    return out

def list2html(l):
    out=""
    for item in l:
        out+=str(item)+"<br>"
    return out

def form2html(l):
    out=""
    for key in l.keys():
        out+=str(key)+" - "+l[key].value+"<br>"
    return out

def timeStamp(d=None):
    if d==None: d=datetime.datetime.now()
    stamp=d.strftime("%Y-%m-%d %H:%M:%S")
    return stamp

def doReps(data):
    data=data.replace("~timestamp~",timeStamp())
    return data

def addEdges(data,replaceToo=True):
    top=fileRead(pageFolder+'top.html')
    bot=fileRead(pageFolder+'bot.html')
    if replaceToo==True:
        data=doReps(data)
    data=top+data+bot
    return data

def tableIt(data):
    top='<table class="bigtable"><tr><td>'
    bot='</td></tr></table>'
    return top+data+bot

def fileWrite(data,fname=pageFolder+"out.html"):
    print "writing to",fname
    f=open(fname,'w')
    f.write(data)
    f.close()

def fileRead(fname,textFile=False):
    f=open(fname)
    raw=f.read()
    f.close()
    if textFile==True and ".txt" in fname:
        raw=raw.replace("\n","\n<br>")
        raw="<code>"+raw+"</code>"
        raw=tableIt(raw)
    return raw


