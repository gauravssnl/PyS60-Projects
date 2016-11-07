
#ipviewer.py script by gauravssnl for PyS60 app IPViewer v1.3

#Use:This Script finds your Local IP and saves the logs to C://IPViewer_log.txt

#How to Run:This script can be easily run in IPro IDE.you should have ipviewer.py & Console.py in the same directory folder like IPViewer

#Program code begins here
 
# ipviewer v1.3 script by gauravssnl
import appuifw,e32,os,sys,re,globalui
dir=appuifw.app.full_name()[0]
path=dir+":\\System\\Apps\\IP Viewer\\"
# print path
sys.path.append(path)
import Console
import socket
try:
    import miso
    miso_import =1
except:
    pass    
lock=e32.Ao_lock()
title="IP Viewer v1.3"
ru= lambda txt:txt.decode("utf-8","ignore")
ur= lambda txt:txt.encode("utf-8","ignore")
configfile=path+"config.ini"
logfile="C:\\IPViewerlog.txt"
ss="Simple Server_0xe247d320.exe"

class Settings(object):
    def __init__(self):
        self.APN= -1
        self.IPHUNT= "100."
        self.RUNSS= 1
        self.VIBRATE= 1
        try:
            self.load()
        except:
            self.save()
            self.load()
    def load(self):
         for name,value in [line.split("=") for line in open(configfile,"r").read().splitlines()] :
             self.__dict__[name]= eval(value)
    def save(self):
         data= ""
         for name in self.__dict__.keys():
             line = name+"="+repr(self.__dict__[name])+"\r\n"
             data += line
         try:
             open(configfile,"w").write(data)
         except:
             if not os.path.exists(path):
                 os.mkdir(path)
                 open(configfile,"w").write(data)    
         del data
                             
class UI(object):
    def __init__(self):
        self.lock=e32.Ao_lock()
        self.sets=Settings()
        self.timert=e32.Ao_timer()
        self.timerip=e32.Ao_timer()
        self.apid_list=[-1]+[ap["iapid"] for ap in socket.access_points() ]
        self.ap_list=[u"Ask User"]+ [ap["name"] for ap in socket.access_points()]
        self.i=1
        self.yesno=[ru("No"),ru("Yes")]
        self.count= 0
        self.developer="gauravssnl"
        
    def select_apn(self):
        appuifw.app.title = ru("Select APN")
        self.id=socket.select_access_point()
        appuifw.app.title = ru(title)
    def app(self):
        appuifw.app.title=ru(title)
        appuifw.app.exit_key_handler=self.exit
        self.i=1
        self.console=Console.Console(True)
        self.text=self.console.text
        appuifw.app.body=self.console.text
        self.text.color=255,0,0
        self.text.font= "title",20
        self.write("%s by %s"%(title,self.developer))
        self.text.color=0,0,0
        self.text.font= "title",18
        if  not len(socket.access_points()):
            self.write("No Access Point is defined.Please add new APN.App will exit")
            e32.ao_sleep(2)
            os.abort()
        else:
            pass    
        self.write("Access Point: %s"%self.ap_list[self.apid_list.index(self.sets.APN)])
        self.write("Find IP:%s"%self.insta(self.sets.IPHUNT))
        self.write("Run Simple Server: %s"%self.yesno[self.sets.RUNSS])
        appuifw.app.menu=[(ru("Start"),self.start),(ru("Settings"),self.settings),(ru("About"),self.about),(ru("Exit"),self.exit)]
        
        
    def clear(self):
        self.text.clear()
        self.text.color=255,0,0
        
        self.text.font= "title",20
        self.write("%s by %s"%(title,self.developer))
        self.text.color=0,0,0
        self.text.font= "title",18
        self.write("Access Point: %s"%self.ap_list[self.apid_list.index(self.sets.APN)])
        self.write("Find IP:%s"%self.insta(self.sets.IPHUNT))
        self.write("Run Simple Server: %s"%self.yesno[self.sets.RUNSS])
        
    def start(self):
        self.clear()
        if self.sets.APN == -1:
            self.select_apn()
            if self.id ==None:
                
                self.write("Please Select Access Point")
            else:
                    self.findip()
        else :
            self.id=self.sets.APN
            self.findip()
    def findip(self):
       appuifw.app.menu=[(ru("Stop"),self.stop),(ru("Exit"),self.exit)]
       self.timert.cancel()
       self.compress()
       try:
           self.apn=socket.access_point(self.id)
           self.apn.start()
           appuifw.app.title=ru("Finding IP...")
           self.ip=str(self.apn.ip())
           self.text.color=0,200,200
           if self.i >200:
               self.i=1
               self.stop()
               self.app()
               return
           self.console.write("%s.IP: "%self.i)
           self.text.color=0,0,255
           self.console.write("%s "%self.ip)
           self.i +=1
           self.ipfound=self.ip.find(self.sets.IPHUNT)
           if self.sets.IPHUNT  and self.ipfound == 0:
               self.text.color=255,0,0
               self.console.write("<Found>")
               if self.sets.VIBRATE and miso_import:
                   try:
                       miso.vibrate(50,100)
                   except:
                      self.sets.VIBRATE=0
                      self.sets.save()
                      pass
               self.timert.cancel()
               self.timertitle("IP Found")
               self.compress()
               self.text.color=0
               self.console.write("\n")
               self.savelog()
               self.timerip.cancel()
               if self.sets.RUNSS:
                   e32.ao_sleep(0.5)
                   #appuifw.note(u"Launching Simple Server")
                   e32.ao_sleep(0.5)
                   try:
                       e32.start_exe(ss,'')
                   except:
                      try:
                          e32.start_exe("E:\\Sys\\bin\\"+ss,'')
                      except:
                          try:
                              e32.start_exe("F:\\Sys\\bin\\"+ss,'')
                          except:
                             appuifw.note(u"Simple Server is not Installed or Unknown Error","error")
                             self.sets.RUNSS=0
                             self.sets.save()    
                           
           else:
               self.console.write("\n")
               self.apn.stop()
               self.savelog()
               self.compress()
               self.timerip.after(1,self.findip)
       except:
           self.write("No Network or Unknown Error")
           appuifw.app.menu=[(ru("Start"),self.start),(ru("Settings"),self.settings),(ru("About"),self.about),(ru("Exit"),self.exit)]
           pass    
           
    def stop(self):
        self.timert.cancel()
        self.apn.stop()
        
        self.timerip.cancel()
        
        self.timert.cancel()
        self.compress()
        appuifw.app.title=ru(title)
        appuifw.app.menu=[(ru("Resume"),self.findip),(ru("Settings"),self.settings),(ru("Clear Log"),self.clear),(ru("About"),self.about),(ru("Exit"),self.exit)]  
                
    def write(self,text):
        self.console.write(ur(text)+"\r\n")
    def insta(self,txt):
        if txt:
            return txt
        else:
            return "<None>"
    def settings(self):
         #self.console=Console.Console(False)
         self.timert.cancel()
         self.timerip.cancel()
         appuifw.app.title=ru(title)
         data=[(ru("Access Point: "),self.ap_list[self.apid_list.index(self.sets.APN)]),(ru("Find IP: "),ru(self.insta(self.sets.IPHUNT))),(ru("Run Simple Server: "),self.yesno[self.sets.RUNSS]),(ru("Vibrtion Alert:"),self.yesno[self.sets.VIBRATE])]
         self.list=appuifw.Listbox(data,self.handle)
         appuifw.app.body=self.list
         appuifw.app.exit_key_handler=self.app
         appuifw.app.menu=[(u"Back",self.app),(u"About",self.about),(u"Exit",self.exit)]
    def handle(self):
         self.current=self.list.current()
         if self.current==0:
             q=appuifw.popup_menu(self.ap_list,u"Access Point:")
             if q!=None and int(q)!=self.sets.APN :
                 self.sets.APN= self.apid_list[int(q)]
                 self.sets.save()
                 self.settings()  
         if self.current==1:
             self.getconfigtext()
         if self.current==2:
             q=appuifw.popup_menu(self.yesno,u"Run Simple Server: ")      
             if q!=None and int(q) !=self.sets.RUNSS:
                 self.sets.RUNSS= int(q)
                 self.sets.save()
                 self.settings()
         if self.current==3:
             q=appuifw.popup_menu(self.yesno,u"Vibration Alert: ")      
             if q!=None and int(q) !=self.sets.VIBRATE:
                 self.sets.VIBRATE= int(q)
                 self.sets.save()
                 self.settings()        
                 
         
             
    def getconfigtext(self):
        self.body=appuifw.Text()
        self.body.color=0
        self.body.font="title",19
        appuifw.app.exit_key_handler=self.saveconfigtext
        if self.current==1:
            appuifw.app.title=ru("Find IP: ")
            self.body.add(ru(self.sets.IPHUNT))
        appuifw.app.body=  self.body
        appuifw.app.menu=[(ru("Save"),self.saveconfigtext),(ru("Back"),self.settings)]
    def saveconfigtext(self):
        val=str(self.body.get()).strip()[:15]
        val=val.replace(" ","")
        
        if val:
            if not val.endswith("."):
                val=val+"."
            if val.count(".")>3:
                val=val[:-1]
        if re.search("([^0123456789.])|(\.\.)",val):
            appuifw.note(u"Settings not saved.Invalid Input")
        else:
            if self.current==1:
                self.sets.IPHUNT=val
                self.sets.save()
        
        self.settings()      
                                  
    def about(self):
        e32.ao_sleep(0.01)
        
        globalui.global_msg_query(ru('Developer:\ngauravssnl(Gaurav Singh)\r\nIP Viewer Log Path:\nC://IPViewerlog.txt\nTo view all  different IP properly,please close/diconnect other application which is connected to internet.you can set Find IP to find particular IP.Example: 100.85. OR 100.105. OR 10.100.\nHappy Phreaking.'), ru('IP Viewer v1.3'))
    def exit(self):
        
        q=appuifw.query(u"Do you really want to Exit","query")
        if q:
            try:
                self.timerip.cancel()
                self.timert.cancel()
                appuifw.app.set_exit()
            except:
                os.abort()
    def savelog(self):
        data=self.console.text.get()
        data=[ur(data) for data in data.splitlines()]
        data="\n".join(data)
        open(logfile,"w").write(data)
        del data
    def timertitle(self,text):
        self.timert.cancel()
        appuifw.app.title=ru(text[:self.count])
        self.count +=1
        if self.count > len(text)+1 :
            self.count=0
            self.timert.cancel()
            appuifw.app.title=ru(title)
            e32.ao_sleep(0.5)
           
        self.timert.after(0.09,lambda : self.timertitle(text))
            
    def compress(self):
        if miso_import:
            try:
                miso.compress_all_heaps()
                #appuifw.note(u"Co")
            except:
                pass
        else:
            pass                
                            
            
        
        
e32.ao_yield()
ui=UI()
ui.app()
