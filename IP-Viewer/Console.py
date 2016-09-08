
#Console.py script for PyS60

import sys
import e32
import appuifw
ru = lambda text, : text.decode('utf-8', 'ignore') 
class Console :


    __module__ = __name__
    def __init__(self, logger = False):
        self.logger = logger
        from e32 import Ao_lock as Ao_lock
        from key_codes import EKeyEnter as EKeyEnter
        self.input_wait_lock = Ao_lock()
        self.input_stopped = False
        self.control = self.text = appuifw.Text()
        self.text.font = ('title', 16, None)
        self.text.color = 0
        self.savestderr = sys.stderr
        self.savestdout = sys.stdout
        self.savestdin = sys.stdin
        sys.stderr = self
        sys.stdout = self
        sys.stdin = self
        self.writebuf = []
        self._doflush = self.clear()
        self._flushgate = self.clear()
        if self.logger : 


            def make_flusher(text, buf):


                def doflush():
                    text.set_pos(text.len())
                    text.add(ru(''.join(buf)))
                    del buf[:]


                return doflush


            self._doflush = make_flusher(self.text, self.writebuf)
            self._flushgate = e32.ao_callgate(self._doflush)
        else : 
            self.logger = False
            self.clear()
        return None




    def __del__(self):
        sys.stderr = self.savestderr
        sys.stdout = self.savestdout
        sys.stdin = self.savestdin
        self.control = self.text = None
        return None




    def stop_input(self):
        self.input_stopped = True
        self.input_wait_lock.signal()




    def clear(self):
        self.text.clear()




    def write(self, obj):
        self.writebuf.append(obj)
        self.flush()




    def writelines(self, list):
        self.write(''.join(list))




    def flush(self):
        if len(self.writebuf) > 0 : 
            if e32.is_ui_thread() : 
                self._doflush()
            else : 
                self._flushgate()
            pass




    def readline(self):
        if  not (e32.is_ui_thread()) : 
            raise IOError('Cannot call readline from non-UI thread')
        pos = self.text.get_pos()
        len = self.text.len()
        save_exit_key_handler = appuifw.app.exit_key_handler
        appuifw.app.exit_key_handler = self.stop_input
        self.input_wait_lock.wait()
        appuifw.app.exit_key_handler = save_exit_key_handler
        if self.input_stopped : 
            self.text.add(u'\n')
            self.input_stopped = False
            raise EOFError
        new_pos = self.text.get_pos()
        new_len = self.text.len()
        if (new_pos <= pos | (new_len - len) != (new_pos - pos)) : 
            new_pos = self.text.len()
            self.text.set_pos(new_pos)
            self.text.add(u'\n')
            user_input = ''
        else : 
            user_input = self.text.get(pos, ((new_pos - pos) - 1))
        return user_input.encode('utf8')



