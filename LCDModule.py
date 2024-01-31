from Components import *
from signal import pause, signal, SIGTERM, SIGHUP
from rpi_lcd import LCD as LCD_C
import time
import threading


class LCD(Component):

    def __init__(self):
        super().__init__('LCD')
        self.lcd = LCD_C()
        self.cond_var.set()
        self.cond_var_support_lock.release()
        self.last_message = ['', '']
        self.line = 1
        signal(SIGTERM, self.safe_exit)
        signal(SIGHUP, self.safe_exit)
        self.write_event = threading.Event()

    def safe_exit(self, signum, frame):
        self.lcd.clear()
        exit(1)

    def active_mode(self):
        print('In Active Mode Buzzer')
        while True:
            self.write_event.wait()
            try:
                self.lcd.text(self.last_message[self.line - 1], self.line)
            except KeyboardInterrupt as err:
                print('Interrupt at ' + self.component_name + ' :\n' + err.args[0])
            finally:
                self.write_event.clear()

    def signal(self, message):
        self.line = message.meta_data['line']
        self.last_message[self.line-1] = message.content
        while self.write_event.is_set():
            continue
        self.write_event.set()

    def listen(self):
        return None




#lcd = LCD()

#m = Message('test', {'line': 1})

#lcd.signal(m)
#time.sleep(3)
#m.content = 'test2'
#m.meta_data['line'] = 2
#lcd.signal(m)
#time.sleep(3)

#m.content = 'test3'
#m.meta_data['line'] = 1
#lcd.signal(m)
#time.sleep(5)

