import sqlite3
import time

from pagebuilder import *

def padLeft(s,goal,wit=" "):
    while len(s)<goal: s=wit+s
    return s

def padRight(s,goal,wit=" "):
    while len(s)<goal: s=s+wit
    return s

class collLogger():
    
    def __init__(self):
        self.con=sqlite3.connect('scr.db')
        self.c=self.con.cursor()
        self.table='qsos'

    def allCalls(self,header=True):
        query="SELECT * FROM %s ORDER BY id DESC"%(self.table)
        results=self.runQuery(query)
        if header==False: return results
        header="ID,Time,Call,Freq,Mode,Sent,"
        header+="Got,QTH,Class,Operator,Notes"
        header=[header.split(",")]
        return header+results

    def logCabrillo(self):
        out=""
        out+="START-OF-LOG: 3.0\nCONTEST: ARRL-SCR\nCATEGORY-STATION: CLASS-S-UN\nCALLSIGN: W4DFU\n"
        lines=self.allCalls(False)
        for line in lines:
            line=list(line)
            for i in range(len(line)):
                if line[i]==None: line[i]=''
            ID,Time,Call,Freq,Mode,Sent,Got,QTH,Class,Op,Nt=line
            if (Mode=="SSB" or Mode=="FM") : Mo="PH"
            else: Mo="CW"
            t=time.strptime(Time, "%Y-%m-%d %H:%M:%S")
            utc=local_to_utc(t)
            print t
            print utc
            Freq="%.03f"%Freq
            Sent=str(Sent)
            Got=str(Got)
            Op=str(Op)
            
            utc=datetime.datetime(*utc[:6])
            tDay=utc.strftime("%Y-%m-%d")
            tTime=utc.strftime("%H%M")
            if len(QTH)>2: QTH="DX"
            
            out+="QSO: "
            out+=padLeft("%d"%(float(Freq)*1000),5)+" "
            out+=Mo+" "
            out+=tDay+" "
            out+=tTime+" "
            out+=padRight("W4DFU",13)+" "
            out+=padRight(Sent,3)+" "
            out+="S"+" "
            out+="FL"+" "
            out+=padRight(Call,13)+" "
            out+=padRight(Got,3)+" "
            out+=Class+" "
            out+=QTH+" "
            out+="\n"
            out=out.upper()
            
        return out

    def logAdif(self):
        out=""
        lines=self.allCalls(False)
        for line in lines:
            line=list(line)
            for i in range(len(line)):
                if line[i]==None: line[i]=''
            ID,Time,Call,Freq,Mode,Sent,Got,QTH,Class,Op,Nt=line
                    
            t=time.strptime(Time, "%Y-%m-%d %H:%M:%S")
            utc=local_to_utc(t)
            print t
            print utc
            Freq="%.03f"%Freq
            Sent=str(Sent)
            Got=str(Got)
            Op=str(Op)
            
            utc=datetime.datetime(*utc[:6])
            tDay=utc.strftime("%Y%m%d")
            tTime=utc.strftime("%H%M")
                        
            out+="<CALL:%d>%s\n"%(len(Call),Call)
            out+="<FREQ:%d>%s\n"%(len(Freq),Freq)
            out+="<MODE:%d>%s\n"%(len(Mode),Mode)
            out+="<QTH:%d>%s\n"%(len(QTH),QTH)
            out+="<RST_RCVD:%d>%s\n"%(len(Got),Got)
            out+="<RST_SENT:%d>%s\n"%(len(Sent),Sent)
            out+="<QSO_DATE:%d>%s\n"%(len(tDay),tDay)
            out+="<TIME_ON:%d>%s\n"%(len(tTime),tTime)
            out+="<OPERATOR:%d>%s\n"%(len(Op),Op)
            out+="<STATION_CALLSIGN:5>W4DFU\n"
            out+="<OWNER_CALLSIGN:5>W4DFU\n"
            out+="<APP_DXKEEPER_MY_QTHID:19>D11-27 Club Station\n"
            out+="<eor>\n\n"
            
        return out

    def oneCall(self,call):
        call=call.replace("'","")
        query="SELECT * FROM %s WHERE call='%s' "%(self.table,call)
        query+="ORDER BY id DESC"
        results=self.runQuery(query)
        header="ID,Time,Call,Freq,Mode,Sent,"
        header+="Got,QTH,Class,Operator,Notes"
        header=[header.split(",")]
        return results
    
    def oneID(self,theID):
        theID=theID.replace("'","")
        query="SELECT * FROM %s WHERE id='%s' "%(self.table,theID)
        results=self.runQuery(query)
        header="ID,Time,Call,Freq,Mode,Sent,"
        header+="Got,QTH,Class,Operator,Notes"
        header=[header.split(",")]
        return header+results


    def getStats(self):
        stats={}
        query="SELECT COUNT (*) FROM %s"%(self.table)
        stats["qsos"]=self.runQuery(query)[0][0]
        
        query="SELECT COUNT (*) FROM %s WHERE mode='SSB'"%(self.table)
        stats["phone"]=self.runQuery(query)[0][0]
		# adding additional query here to get FM stats and summing with SSB
        query="SELECT COUNT (*) FROM %s WHERE mode='FM'"%(self.table)
        stats["phone"] = stats["phone"] + self.runQuery(query)[0][0]
        stats["dig"]=stats["qsos"]-stats["phone"]

        query="SELECT COUNT (DISTINCT qth) FROM %s"%(self.table)
        stats["locations"]=self.runQuery(query)[0][0]
        
        query="SELECT COUNT (*) FROM %s WHERE class='S'"%(self.table)
        stats["schools"]=self.runQuery(query)[0][0]

        query="SELECT COUNT (*) FROM %s WHERE class='C'"%(self.table)
        stats["clubs"]=self.runQuery(query)[0][0]

        query="SELECT DISTINCT qth FROM %s"%(self.table)
        stats["loclist"]=list(self.runQuery(query))

        stats["mult"]=stats["locations"]+stats["clubs"]*2+stats["schools"]*5
        stats["qsopoints"]=stats["phone"]+stats["dig"]*2
        stats["score"]=stats["mult"]*stats["qsopoints"]
        
        return stats

    def delById(self,theID):
        theID=theID.replace("'","")
        query="DELETE FROM %s WHERE id='%s' "%(self.table,theID)
        self.runQuery(query,True)
        return
    
    def delEverything(self):
        query="DELETE FROM %s"%(self.table)
        self.runQuery(query,True)
        return

    def changeIt(self,data):
        print data
        query="UPDATE %s SET "%self.table
        for key in data.keys():
            if key=='action': continue
            if not key in ['sent','got','freq','id']:
                if data[key]==None: data[key]=''
                if data[key]=='NONE': data[key]=''
                data[key]="'"+data[key]+"'"
            query += "%s=%s, "%(key,data[key])
        query+="WHERE id=%s"%data["id"]
        query=query.replace(", WHERE", " WHERE")
        self.runQuery(query,True)
        return
    
    def addQso(self,formDict):
        if not 'stamp' in formDict.keys():
            formDict['stamp']=timeStamp()
        cols,vals="",""
        for key in formDict.keys():
            if not key in ['got','sent','freq']:
                formDict[key]="'"+formDict[key]+"'"
            if key=='action': continue
            cols+=key+", "
            vals+=formDict[key]+", "
        query="INSERT INTO %s (%s) VALUES (%s);"%(self.table,cols,vals)
        query=query.replace(", )",")")
        self.runQuery(query,True)
        return
    
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
    
    def commit(self):
        print "saving changes to database"
        self.con.commit()
        
    def disconnect(self):
        self.con.close()

