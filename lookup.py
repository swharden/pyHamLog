import sqlite3

class lookupDb:

    def lookupCall(self,call):
        query='SELECT * from calldb WHERE call="%s";'%call
        data=self.c.execute(query).fetchone()
        if data==None: return None
        call,name,addr,city,state,zipc=data
        return [call,name,addr,city,state,zipc]

    def locCall(self,call,countryOnly=True):
        while len(call)>0:
            query='SELECT * from locs WHERE call="%s";'%call
            data=self.c.execute(query).fetchone()
            if not data==None: break
            call=call[:-1]
        prefix,country,continent,latitude,longitude,star,itu,cq=data
        if countryOnly: return country
        else: return data

    def htmlLookup(self,call):
        out="""<html>
        <body onload="window.top.enter.qth.value='~';">
        <br><b>%s</b><br>@</body></html>"""%(call)  
        country=self.locCall(call)
        if country=="USA":
            callInfo=self.lookupCall(call)
            if callInfo==None:
                out=out.replace("@","no info")
                out=out.replace("~","")
                return
            call,name,addr,city,state,zipc=callInfo
            msg="%s<br>%s, %s, USA"%(name,city,state)
            out=out.replace("@",msg)
            out=out.replace("~",state)
            return out
        else:
            out=out.replace("@",country)
            out=out.replace("~",country)
            return out
    
    def connect(self):
        print "connecting to local lookup database"
        self.con=sqlite3.connect('./data/db.sqlite')
        self.c=self.con.cursor()
        self.table='locs'
        
    def disconnect(self):
        self.con.close()
