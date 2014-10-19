## Created 2012 by Scott Harden, AJ4VD
## Updated October 19, 2014 by Andrew Milluzzi, KK4LWR, andy@gatorradio.org
## Report bugs to: andy@gatorradio.org

## Edits:
## - Fixed bug when running "deleteAll" that cased page not log
## - Changed "deleteAll" page to point back to admin panel instead of log
## - Added instructions for configuring IP address. See comment around line 250

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import urlparse
import cgi
import os.path

from database import *
from pagebuilder import *
from lookup import *


class Handler(BaseHTTPRequestHandler):

    def do_PAGE(self,form=None,msg="",edge=True):
        if self.path=="/": self.path="/index.html"
        fname=pageFolder+self.path
        page=""
        ### BUILD THE PAGE HERE ###

        if not form==None:
            formDict={}
            for key in form.keys():
                formDict[key]=form[key].value
                if key=='call':
                    formDict[key]=formDict[key].upper()
            #msg+=tableIt("GOT FORM:<br>"+form2html(form))

        if self.path=="/viewlog":
            logger=collLogger()
            page='<div align="center">'
            page+=results2html(logger.allCalls(),editable=False)
            page+="</div>"
            logger.disconnect()
            msg+=page

        elif self.path=="/viewlogedit":
            logger=collLogger()
            page='<div align="center">'
            page+=results2html(logger.allCalls())
            page+="</div>"
            logger.disconnect()
            msg+=page
            
        elif self.path=="/viewscores":
            logger=collLogger()
            msg+=stats2html(logger.getStats())
            logger.disconnect()
            
        elif self.path=="/genfigs":
            os.system('genstats.py')
            msg="GENERATED!<br>"
            msg+='<a href="adminsrock.html">return to admin page</a>'
            
        elif self.path=="/viewops":
            logger=collLogger()
            ops=logger.runQuery("select distinct operator from qsos;")
            msg+="<h2>OPERATORS</h2>"
            for op in ops:
                msg+="<hr>"
                
                msg+='<b><a href="http://www.qrz.com/db/%s">%s</a></b><br>'%(str(op[0]),str(op[0]))
                
                query="select count(*) from qsos where operator='%s';"%op
                results=logger.runQuery(query)[0]
                msg+="%d QSOs<br>"%(int(results[0]))

                query="select count(distinct qth) from qsos where operator='%s';"%op
                results=logger.runQuery(query)[0]
                msg+="%d states/provinces/countries<br>"%(int(results[0]))


                query="select count(*) from qsos where operator='%s' and class='I';"%op
                results=logger.runQuery(query)[0]
                msg+="%d individuals contacted<br>"%(int(results[0]))

                query="select count(*) from qsos where operator='%s' and class='C';"%op
                results=logger.runQuery(query)[0]
                msg+="%d clubs contacted<br>"%(int(results[0]))
                
                query="select count(*) from qsos where operator='%s' and class='S';"%op
                results=logger.runQuery(query)[0]
                msg+="%d schools contacted<br>"%(int(results[0]))
                
            logger.disconnect()
            msg+="<hr>"
            
        elif 'lookup-' in self.path:
            call=self.path.split("-")[1]
            LDB=lookupDb()
            LDB.connect()
            msg+=LDB.htmlLookup(call.upper())
            LDB.disconnect()
            #msg+=genHtmlFor(call)
            
        elif self.path=="/sample":
            msg+=fileRead(pageFolder+"postform.html")
            logger=collLogger()
            page='<br><br><div align="center">'
            page+=results2html(logger.allCalls())
            page+="</div>"
            logger.disconnect()
            msg+=page
            
        elif "act-edit" in self.path:
            theID=self.path.split("-")[-1]
            if form==None:
                #display that line
                logger=collLogger()
                results=logger.oneID(theID)
                logger.disconnect()
                msg+=results2editable(results)
            else:
                #actually change that line
                logger=collLogger()
                logger.changeIt(formDict)
                msg='<br><br><div align="center">'
                msg+="<h2>Changes made:</h2>"
                msg+=results2html(logger.oneID(theID))
                msg+="</div>"
                logger.disconnect()
            
        elif self.path=="/act-add":
            if form==None:
                msg+="NO STUFF?!?"
            elif "LOG" in formDict["action"]:
                logger=collLogger()
                logger.addQso(formDict)
                msg+='<h2>ADDED QSO</h2>'
                call=formDict["call"]
                
                header="ID,Time,Call,Freq,Mode,Sent,"
                header+="Got,QTH,Class,Operator,Notes"
                header=header.split(",")
        
                msg+=results2html([header]+logger.oneCall(call));
                logger.disconnect()
                
            elif "chk" in formDict["action"]:
                call=formDict["call"]
                logger=collLogger()
                results=logger.oneCall(call)
                logger.disconnect()
                print results
                if len(results)==0:
                    msg+="<br><h2>NEW CALLSIGN:<br>"+call+"</hr>"
                else:
                    msg+='MATCHES FOR: %s<br>'%call
                    msg+=tableIt(results2html(results))
                    
            else:
                msg="UNKNOWN ACTION"
                
        elif "act-delete" in self.path:
            theID=self.path.split("-")[-1]
            msg+="Are you SURE you want to delete the following?<br>"
            logger=collLogger()
            msg+=results2html(logger.oneID(theID),editable=False)
            logger.disconnect()
            msg+='<a href="act-delsure-%s">YES, DELETE IT!</a>'%theID

        elif "deleteAll" in self.path:
            #theID=self.path.split("-")[-1]
            logger=collLogger()
            logger.delEverything()
            logger.disconnect()
            msg+='<br><br><h2>DELETED EVERYTHING!!!<h2>'
            msg+='<a href="adminsrock.html">return to admin page</a>'
            
        elif "act-delsure" in self.path:
            theID=self.path.split("-")[-1]
            logger=collLogger()
            logger.delById(theID)
            logger.disconnect()
            msg+='<br><br><h2>DELETED ID: %s<h2>'%theID
            msg+='<a href="viewlog">return to log</a>'

        elif "unique" in self.path:
            codes=[]
            dups=[]
            logger=collLogger()
            for item in logger.allCalls(header=False):
                code="%s-%2d-%s"%(item[2],item[3],item[4])
                code=code.upper()
                if code in codes: dups.append(code)
                codes.append(code)           
            logger.disconnect()
            msg+="<br><br><b>Duplicates:</b><br>"
            for code in dups: msg+=code+", "
            msg+="<br><br><b>All Codes:</b><br>"
            msg+='<span style="font-size:8px;">'
            for code in codes: msg+=code+", "
            msg+='</span>'
            
        elif "adif.txt" in self.path:
            logger=collLogger()
            msg=logger.logAdif()
            logger.disconnect()
            edge=False
            
        elif "cabrillo.txt" in self.path:
            logger=collLogger()
            msg=logger.logCabrillo()
            logger.disconnect()
            edge=False
        elif '.png' in self.path:
            f=open("./pages/"+self.path,'rb')
            msg=f.read()
            f.close()
            edge=False
            
        elif '.' in self.path and os.path.exists(fname):
            msg=fileRead(fname,True)
            if "frameset" in msg: edge=False
        else:
            msg="<h3>UNKNOWN PATH:<br>[%s]</h3><br>"%self.path
            
        ### SERVE THE PAGE ###
        if edge==True:
            msg=addEdges(msg)
        self.wfile.write(msg)
        
    
    def do_GET(self):
        if 'favicon' in self.path:
            self.send_error(404, "File not found")
            return    
        self.send_response(200)
        self.end_headers()
        self.do_PAGE()
        return

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                            environ={'REQUEST_METHOD':'POST',
                            'CONTENT_TYPE':self.headers['Content-Type'],})
        self.send_response(200)
        self.end_headers()
        self.do_PAGE(form)
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

	
## Edit the section below for your computer IP and port settings
if __name__ == '__main__':
    myIP='localhost'
    myIP='192.168.1.200'
    myPort=80
    server = ThreadedHTTPServer((myIP, myPort), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    print 'http://%s:%d'%(myIP,myPort)
    server.serve_forever()
