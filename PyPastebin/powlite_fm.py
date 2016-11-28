#-*- encoding:utf-8 -*-
'''name:powlite_fm
文件管理模块，支持触屏
by爱不只是说说
2011/07/01
'''
cn = lambda x:x.decode('u8')

class manager:
    __name__ == 'powlite_fm'
    def __init__(s, filepath=None):
        import os
        import appuifw
        try:
            import cfileman
            s.CF = cfileman.FileMan()
            s.EA, s.ES = cfileman.EAttMatchMask, cfileman.ESortByName
        except:s.CF = None
        s.A, s.E, s.O = appuifw, appuifw.e32, os
        s.lock = s.E.Ao_lock()
        s.path = None
        if type(filepath) == unicode:
            filepath = filepath.encode('u8')
        s.filepath = filepath
        del filepath

    def main(s, __Listing=[]):
        if s.path:
            s.A.app.title=cn(s.path)
        else:
            s.A.app.title=cn('文件管理')
        seat = s.A.selection_list(__Listing, 1)
        if seat <> None:
            if seat == 0:
                if __Listing[0] == u'<<<':
                    s.path = s.path[:-len(s.path.split('\\')[-2])-1]
                elif __Listing[0] == cn('最近打开'):
                    s.A.app.title=cn('最近打开')
                    __Listing = []
                    if s.filepath and s.O.path.isfile(s.filepath) and s.find == 'file':
                        __Listing = [cn(i.replace('\r\n','')) for i in open(s.filepath).readlines()  if s.O.path.isfile(i)]
                        if s.ext:
                            __Listing = [i for i in __Listing if s.O.path.splitext(i)[1].lower() in s.ext]
                    elif s.filepath and s.O.path.isfile(s.filepath) and s.find == 'dir':
                        __Listing = [cn(i.replace('\r\n','')) for i in open(s.filepath).readlines() if s.O.path.isdir(i)]
                    if s.find == 'file':
                        __list = [u'<<<']
                        if __Listing:
                            for i in __Listing:
                                path = s.O.path.split(i.encode('u8')) 
                                __list += [cn('%s 位于 %s'%(path[1], path[0]))]
                            del path
                        __seat = s.A.selection_list(__list, 1)
                        if __seat:
                            if s.markmod:
                                __seat = s.A.multi_selection_list(__list[1:], search_field = 1)
                                if __seat:
                                    s.path = [__Listing[i] for i in __seat]
                                    s.quit(1)
                                    return
                            else:
                                s.path = __Listing[__seat-1]
                                s.quit(1)
                                return
                    elif s.find == 'dir':
                        __seat = s.A.selection_list([u'<<<']+__Listing, 1)
                        if __seat:
                            if s.markmod:
                                __seat = s.A.multi_selection_list(__Listing, search_field = 1)
                                if __seat:
                                    s.path = [__Listing[i] for i in __seat]
                                    s.quit(1)
                                    return
                            else:
                                s.path = __Listing[__seat-1]
                                s.quit(1)
                                return
            else:
                if not s.path:
                    s.path = __Listing[seat].encode('u8')+'\\'
                elif seat == 1 and s.find == 'dir':
                    if s.markmod:
                        __list = __Listing[2:]
                        if __list:
                            __seat = s.A.multi_selection_list(__list, search_field = 1)
                            if __seat:
                                s.path = [cn(s.path)+__list[i][1:-1]+u'\\' for i in __seat]
                                s.quit(1)
                                return
                        else:
                            s.A.note(cn('没有可标记目录！'),'error')
                            s.path = s.path[:-len(s.path.split('\\')[-2])-1]
                            del __list
                    else:
                        s.path = cn(s.path)
                        s.quit(1)
                        return
                else:
                    name = __Listing[seat][1:-1].encode('u8')
                    if name:
                        path = s.path+name
                        del name
                    else:path = None
                    if path and s.O.path.isdir(path):
                        s.path = path+'\\'
                        del path
                    else:
                        if s.markmod:
                            __list = [i for i in __Listing[1:] if s.O.path.isfile(s.path+i.encode('u8'))]
                            seat = s.A.multi_selection_list(__list, search_field = 1)
                            if seat:
                                s.path = [cn(s.path)+ __list[i]  for i in seat]
                                s.quit(1)
                                return
                            del __list
                        else:
                            s.path = cn(s.path)+__Listing[seat]
                            s.quit(1)
                            return
            del __Listing
            try:s.scan()
            except:
                s.path = None
                s.scan()

        else:
            if s.back and s.path:
                s.path = s.path[:-len(s.path.split('\\')[-2])-1]
                s.scan()
            else:s.quit()

    def AskUser(s, path = None, find = 'file', ext = [], markmod = False, back = False):
        s.path = path
        s.find = find
        s.ext = ext
        s.markmod = markmod
        s.back = back
        Screen, Title = s.A.app.screen, s.A.app.title
        s.A.app.screen = 'normal'
        if type(s.path) == unicode:
            s.path = s.path.encode('u8')
        if s.path and not s.O.path.isdir(s.path):
            s.path = None
        if s.path:
            s.path = s.path.replace('/','\\')
            if s.path[-1] <> '\\':
                s.path += '\\'
        if s.ext:
            s.ext=[i.lower() for i in s.ext]
        if s.find <> 'dir':
            s.find = 'file'
        try:s.scan()
        except:
            s.path = None
            s.scan()
        s.lock.wait()
        s.A.app.screen, s.A.app.title = Screen, Title
        del Screen, Title
        return s.path

    def scan(s):
        if s.path and not s.O.path.isdir(s.path):
            s.path = None
        if s.path:
            s.A.app.title = cn('请稍后……')            
            __list1, __list2 = [u'<<<'], []
            if s.find == 'dir':
                if s.markmod:__list1 += [cn('☆标记当前目录☆')]
                else:__list1 += [cn('☆选择当前目录☆')]

            if s.CF:
                __list0 = s.CF.listdir(cn(s.path), s.EA, s.ES)
                __list1 += [u'['+i+u']' for i in __list0[0]]
                if s.find == 'file':
                    if s.ext:
                        __list2 = [i for i in __list0[1] if s.O.path.splitext(s.path+i.encode('u8'))[1].lower() in s.ext]
                    else:
                        __list2 = list(__list0[1])

            else:
                __list0 = s.O.listdir(s.path)
                __list1, __list2 = [u'<<<'], []
                if __list0:
                    for i in __list0:
                        if s.O.path.isdir(s.path+i):
                            __list1.append(cn('[%s]'%i))
                        elif s.find == 'file':
                            if s.ext:
                                if s.O.path.splitext(s.path+i)[1].lower() in s.ext:
                                    __list2.append(cn(i))
                            else:
                                __list2.append(cn(i))
            __Listing = __list1+__list2
            del __list0, __list1, __list2
        else:
            if s.CF:
                __list = s.CF.drive_space().keys()
                __list.sort()
                __Listing = [cn('最近打开')]+__list
                del __list
            else:__Listing = [cn('最近打开')]+s.E.drive_list()
        s.main(__Listing)

    def quit(s, x=0):
        if not x:s.path = None
        elif s.filepath and s.path:
            __list0, __list1 = [], []
            if s.O.path.isfile(s.filepath):
                for i in open(s.filepath).readlines():
                    i = i.replace('\r\n','')
                    if s.O.path.isdir(i):
                        __list0.append(i)
                    else:
                        __list1.append(i)
            if s.markmod:
                path = [i.encode('u8') for i in s.path]
                if s.find == 'dir':
                    for i in path:
                        if not i in __list0:
                            __list0 = [i]+__list0
                else:
                    for i in path:
                        if not i in __list1:
                            __list1 = [i]+__list1
            else:
                path = s.path.encode('u8')
                if s.find == 'dir':
                    if not path in __list0:
                        __list0 = [path]+__list0
                else:
                    if not path in __list1:
                        __list1 = [path]+__list1
            __list = __list0[:8]+__list1[:8]
            try:
                a=open(s.filepath,'w')
                [a.write('%s\r\n'%i) for i in __list]
                a.close()
                del a
            except:pass
            del __list, __list0, __list1, path
        s.lock.signal()

if (__name__ == '__main__'):
    filemain=manager(filepath='d:\\file.txt')#初始化，以下函数基于此类
    #manager([filepath=None])
    #filepath：最近打开记录路径，没有则不保存

    print filemain.AskUser(path=None, ext=[], find='file', markmod=0, back=0)
    #AskUser([path=None, ext=[], find='file', markmod=0, back=0])
    #path：初始目录路径
    #ext：过滤文件后缀，多个用,号隔开如ext=['.py', '.pyc']
    #find：选择类型，find='file'查找文件，find='dir'查找目录。
    #markmod：markmod=True时为标记模式
    #back：back=True时按取消将返回上级目录，否则退出