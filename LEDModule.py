from Components import *
import time
import threading
from gpiozero import LED as LED_C

class LED(Component):
    def __init__(self, pin_id):
        super().__init__('LED')
        self.pin_id = pin_id
        self.led = LED_C(self.pin_id)

    def active_mode(self):
        print('In Active Mode LED')
        while True:
            self.led.on()
            self.cond_var.wait(0.5)
            if self.cond_var_support_lock.locked():
                self.led.off()
                print('Exiting Active Mode LED')
                return
            self.led.off()
            self.cond_var.wait(0.5)
            if self.cond_var_support_lock.locked():
                print('Exiting Active Mode LED')
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



#led = LED(18)
#led.signal(Message('on'))
#time.sleep(5)
#led.signal(Message('off'))

#time.sleep(2)

#led.signal(Message('on'))
#time.sleep(3)

#led.signal(Message('off'))
