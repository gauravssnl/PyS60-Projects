# py pastebin  v1.00.1 script by gauravssnl for symbian OS
# pys60 v2.0 script 
import appuifw
import e32
import os
import sys
import os.path
import pastebin_python as P
import powlite_fm
import globalui

lk = e32.Ao_lock()
ru = lambda text : text.decode("utf-8","ignore")
ur = lambda text : text.encode("utf-8","ignore")
config = "PyPastebin.dat"
title = u"Py Pastebin"
expiry_list = [u"Never",u"10 Minutes",u"1 Hour",u"1 Day",u"1 Month"]
privacy_list  = [u"Public",u"Unlisted",u"Private"]
format_list = [u"Python",u"PyS60",u'Text',u"HTML"]
manager = powlite_fm.manager()
class sets(object):
    def __init__(self):
        self.APIKEY = ""
        self.USER = ""
        self.PASS = ""
        self.PTITLE = ""
        self.PFORMAT = 0
        self.PEXPIRY =0
        self.LOGIN= 0
        self.PPRIVACY = 0
        try :
            self.load()
        except :
            self.save()
                
    def load(self):
        try :
            for name,value in [line.split("=") for line in open(config).read().splitlines()] :
                self.__dict__[name] = eval(value)
        except:
            pass
    def save(self):
        data = ""
        for name in self.__dict__.keys() :
            line = name + "=" +repr(self.__dict__[name]) + "\r\n"
            data += line
        open(config,"w").write(data)
        del data

sets = sets()
        
def login_settings():
    data = [(ru("API Key:"),ru(sets.APIKEY)),(ru("Username:"),ru(sets.USER)),(ru("Password:"),ru(sets.PASS))]
    appuifw.app.title = ru(title)
    global list
    list = appuifw.Listbox(data ,lambda :handle())
    appuifw.app.body = list 
    appuifw.app.menu = [(u'Back',app),(u'About',about),(u'Exit',exit)]
    appuifw.app.exit_key_handler = app

def handle():
    global body
    body = appuifw.Text()
    body.color = 0
    
    appuifw.app.body = body
    
    global list
    curr = list.current()
    if curr == 0:
        appuifw.app.title = ru("API Key:")
        body.add(ru(sets.APIKEY))    
    elif curr == 1:
        appuifw.app.title = ru("Username:")
        body.add(ru(sets.USER))
    elif curr == 2 :
        appuifw.app.title = ru("Password:")
        body.add(ru(sets.PASS))
    appuifw.app.menu = [(u'Save',lambda : save_text(curr)),(u'Back',login_settings)]
    appuifw.app.exit_key_handler = lambda : save_text(curr)    

def save_text(curr):
    global body 
    data = ur(body.get())
    if curr == 0:
        data = data.strip().replace(' ','')
        if sets.APIKEY != data :
            sets.APIKEY = data
            sets.LOGIN = 0
            sets.save()
    elif curr == 1:
        data = data.strip().replace(' ','')
        if sets.USER != data :
            sets.USER = data
            sets.LOGIN =0
            sets.save()
    elif curr ==2:
        if sets.PASS != data :
            sets.PASS = data
            sets.LOGIN = 0
            
            sets.save()
    login_settings()

def settings():
    appuifw.app.title = ru(title)
    appuifw.app.menu = [(u'Back',app),(u'About',about),(u'Exit',exit)]
    data = [(ru("Paste Format:"),format_list[sets.PFORMAT]),(ru("Paste Privacy:"),privacy_list[sets.PPRIVACY]),(ru("Paste Expiry:"),expiry_list[sets.PEXPIRY])]
    global slist
    slist = appuifw.Listbox(data,lambda: handles())
    appuifw.app.body = slist
    appuifw.app.exit_key_handler = app
    
    
def handles():
    global slist    
    lcurr = slist.current()
    if lcurr == 0:
        q = appuifw.popup_menu(format_list ,u"Paste Format:" )
        if q is not None and int(q) != sets.PFORMAT :
            sets.PFORMAT = int(q)
            sets.save()
            settings()
    if lcurr == 1:
        q = appuifw.popup_menu(privacy_list ,u"Paste Privacy:" )
        if q  is not None and int(q) != sets.PPRIVACY :
            sets.PPRIVACY = int(q)
            sets.save()
            settings()        
    
    if lcurr == 2:
        q = appuifw.popup_menu(expiry_list ,u"Paste Expiry:" )
        if q is not None and int(q) != sets.PEXPIRY :
            sets.PEXPIRY = int(q)
            sets.save()
            settings()
   
def app():
    global bodi
    appuifw.app.screen = 'normal'
    bodi = appuifw.Text()
    bodi.font = "title",18
    bodi.color = 255,0,0 
    bodi.add(u"Py Pastebin v1.00.1 by gauravssnl\n")
    appuifw.app.title = ru(title)
    appuifw.app.body =bodi
    appuifw.app.exit_key_handler = exit
    bodi.font = "title",16
    bodi.color = 0,0,0
    bodi.add(u'I am just a student who failed in life.\n')
    bodi.add(u'Pastebin made easier.Share codes directly from files.To know more ,Click on "About"\n')
    show()
    if sets.LOGIN ==0:
        if sets.APIKEY =="" or sets.USER =="" or sets.PASS =="":
            bodi.add(u"Go to Settings and enter your API,username and Password\n")
            appuifw.app.menu=[(ru("Login Settings"),login_settings),(u'About',about),(ru("Exit"),exit)]
        else:
            bodi.add(u'>>you are not logged in\n')
            appuifw.app.menu=[(ru("Login"),login),(ru("Login Settings"),login_settings),(ru('Paste Settings'),settings),(u'About',about),(ru("Exit"),exit)]
        
    elif sets.LOGIN ==1:
        bodi.add(ru('>>You are logged in\n'))
        
        appuifw.app.menu=[(ru("Create New Paste"),create),(ru('Paste Settings'),settings),(ru('About'),about),(ru("Exit"),exit)]
        
        
def exit():
    sets.LOGIN = 0
    sets.save()
    os.abort()        
def login():
    global bodi,pastebin
    
    clear()
    bodi.add(u'>>Trying to Log in\n')
    try:
        pastebin = P.PastebinPython(api_dev_key =sets.APIKEY)
        pastebin.createAPIUserKey(sets.USER,sets.PASS)
        bodi.add(u">>Login Successfull\n")
        sets.LOGIN = 1
        sets.save()
        
        appuifw.app.menu=[(ru("Create New Paste"),create),(ru('Paste Settings'),settings),(u'About',about),(ru("Exit"),exit)]
    except Exception,e:
        bodi.add(u'>>Login Failed or Connection Failed\n')
        
        sets.LOGIN = 0
        sets.save()
            
    
def create():
   
    #login()
    
    formatl = ['python','pys60','text','html4strict']
    expiryl = ['N','10M','1H','1D','1M']
    
    if pastebin.api_user_key != '':
        file = manager.AskUser()
        if file:
            bodi.add(u'File:    %s\n'%file)
            ptitle = appuifw.query(u'Paste Title:','text',u'%s'%(os.path.split(file)[1]))
            if ptitle is None :
                ptitle = os.path.split(file)[1]
            bodi.add(u'Paste Title:    %s\n'%ptitle)
            e32.ao_sleep(0.5)
            bodi.add(u'>>Trying to create the Paste\n')
            try:
                pasteurl = pastebin.createPasteFromFile(file,ptitle,formatl[sets.PFORMAT],sets.PPRIVACY,expiryl[sets.PEXPIRY])
                bodi.add (u'>>Paste Created\n')
                bodi.add(u'>>Paste URL: \n%s\n'%pasteurl)
            except :
                try:
                    fd = str(open(file).read())
                    pasteurl = pastebin.createPaste(fd,ptitle,formatl[sets.PFORMAT],sets.PPRIVACY,expiryl[sets.PEXPIRY])
                    bodi.add (u'>>Paste Created\n')
                    bodi.add(u'>>Paste URL: \n%s\n'%pasteurl)
                except:
                    bodi.add(u">>Failed to create paste.Try again.\n")    

def clear():
    global bodi
    bodi.clear()
 
    bodi.font = "title",18
    bodi.color = 255,0,0 
    bodi.add(u"Py Pastebin v1.00.1 by gauravssnl\n")
    
    
    bodi.font = "title",16
    bodi.color = 0,0,0
    show()
    
def show():
    global bodi
    bodi.add(u'-------------Paste Settings  --------------\n')
    bodi.add(ru('Paste Format: %s\n'%format_list[sets.PFORMAT]))
    bodi.add(ru('Paste Privacy: %s\n'%privacy_list[sets.PPRIVACY]))
    bodi.add(ru('Paste Expiry: %s\n'%expiry_list[sets.PEXPIRY]))
    bodi.add(u'----------------------------------------------\n')           
             
def about():
    globalui.global_msg_query(u'This app helps to create new pastes on pastebin.com from files easily.No need to copy and paste your code now.Pastebin is site for sharing codes easily.You need to have a Pastebin account. Log into your pastebin account first and you need to get your own unique API Key from Pastebin by visiting this URL:\nhttp://pastebin.com/api\nThanks to developers of pastebin_python,requests,cgi and other pys60 developers',u'Py Pastebin v1.00.1 beta')
                   
    
                         
e32.ao_yield()       
app()         
lk.wait()

        
        
            

    

