from Components import *
import time
import threading

from gpiozero import Buzzer as BUZZER

class Buzzer(Component):
    def __init__(self, pin_id):
        super().__init__('Buzzer')
        self.pin_id = pin_id
        self.buzzer = BUZZER(self.pin_id)
        self.buzzer.on() 
    
    def active_mode(self):
        print('In Active Mode Buzzer')
        while True:
            self.buzzer.off()
            self.cond_var.wait(1)
            if self.cond_var_support_lock.locked():
                print('Exiting Active Mode Buzzer')
                self.buzzer.on()
                return
            self.buzzer.on()
            self.cond_var.wait(1)
            if self.cond_var_support_lock.locked():
                print('Exiting Active Mode Buzzer')
                return

    def signal(self, message):
        if message.content == 'on':
            if self.cond_var_support_lock.locked():
                self.cond_var_support_lock.release()
                self.cond_var.set()
        elif message.content == 'off':
            if not self.cond_var_support_lock.locked():
                self.cond_var_support_lock.acquire()
                self.cond_var.clear()

    def listen(self):
        return None


#buzzer = Buzzer(20)
#buzzer.signal(Message('on'))
#time.sleep(5)
#buzzer.signal(Message('off'))
