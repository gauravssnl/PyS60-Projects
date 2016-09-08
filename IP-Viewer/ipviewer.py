
#ipviewer.py script by gauravssnl for PyS60 app IPViewer

#Use:This Script finds your Local IP and saves the logs to C://IPViewer_log.txt

#How to Run:This script can be easily run in IPro IDE.you should have ipviewer.py & Console.py in the same directory folder like IPViewer

#Program code begins here
 
import socket
import e32
import appuifw
import globalui
import sys
drive = appuifw.app.full_name()[0]
path = drive + ':\\System\\Apps\\IP Viewer'
sys.path.append(path)
del drive
del path
import Console
console = Console.Console(True)
lk = e32.Ao_lock()
t = 0.5
timer = e32.Ao_timer()
sleep = e32.ao_sleep
ru = lambda txt, : txt.decode('utf-8', 'ignore') 
ur = lambda txt, : txt.encode('utf-8', 'ignore') 
path = 'c:\\IPViewer_log.txt'

def quit():
    timer.cancel()
    appuifw.app.set_exit()




def about():
    e32.ao_sleep(0.1)
    appuifw.app.body = bd
    globalui.global_msg_query(ru('Developer:\ngauravssnl(Gaurav Singh)\r\nIP Viewer Log Path:\nC:\\IPViewer_log.txt\nTo view all  different IP properly,please close other application which connect to internet.'), ru('IP Viewer v1.1'))


def stop():
    appuifw.app.title = u'IP Viewer v1.1'
    timer.cancel()
    bd.color = (255, 0, 0)
    add('Stopped')
    bd.color = 0
    appuifw.app.menu = [(u'Start', lambda  : ip(j) ), (u'Clear Screen', clear), (u'About', about), (u'Exit', quit)]


def save():
    data = bd.get().splitlines()
    data = [ur(data) for data in data]
    data = '\n'.join(data)
    open(path, 'w').write(data)




def add(txt):
    console.write(txt + '\n')



def ip(i = 1):
    global ap, j

    appuifw.app.title = u'Finding IP...'
    appuifw.app.menu = [(u'Stop', stop), (u'Clear Screen', clear), (u'About', about), (u'Exit', quit)]
    if i == 201 : 
        clear()
        i = 1
        timer.cancel()
    ap = socket.access_point(id)
    ap.start()
    bd.color = (0, 200, 200)
    console.write(str(i) + '.IP:  ')
    bd.color = (0, 0, 255)
    console.write(ap.ip() + '\n')
    ap.stop()
    timer.cancel()
    i = (i + 1)
    j = i
    timer.after(1, lambda  :  ip(i) )
    

def clear():
    bd.clear()
    bd.color = 0
    bd.font = ('title', 20)
    bd.color = (255, 0, 0)
    add('IP Viewer v1.1 by gauravssnl')
    bd.color = 0
    bd.font = ('title', 18)




def app():
    global bd, id
    appuifw.app.exit_key_handler = quit
    appuifw.app.title = u'IP Viewer v1.1'
    appuifw.app.menu = [(u'Start', lambda  : app() ), (u'Clear Screen', clear), (u'About', about), (u'Exit', quit)]
    bd = console.text
    appuifw.app.body = bd
    bd.color = (255, 0, 0)
    bd.font = ('title', 20)
    bd.clear()
    add('IP Viewer v1.1 by gauravssnl')
    bd.font = ('title', 18)
    bd.color = (0, 0, 0)
    sleep(t)
    id = socket.select_access_point()
    if id is None : 
        add('Please select Access Point')
    if id : 
        ip()
    

appuifw.app.exit_key_handler = quit
app()
lk.wait()
