from Components import *
import time
import threading

from pad4pi import rpi_gpio


class Keypad(Component):
    KEYPAD = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]

    def __init__(self, row_pins, col_pins):
        super().__init__('Keypad')
        self.row_pins = row_pins
        self.col_pins = col_pins
        self.buffer = []
        self.buffer_size = 512
        self.cond_var.set()
        self.cond_var_support_lock.release()
        self.is_lock = False

    def __init_pins(self):
        self.factory = rpi_gpio.KeypadFactory()
        self.keypad = self.factory.create_keypad(keypad=Keypad.KEYPAD,
                                                   row_pins=self.row_pins,
                                                   col_pins=self.col_pins)

    def handler(self, key):
        if self.is_lock:
            return
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(key)

    def active_mode(self):
        print('In Active Mode ' + self.component_name)
        self.__init_pins()
        while True:
            try:
                self.keypad.registerKeyPressHandler(self.handler)
                while True:
                    time.sleep(0.01)
            except KeyboardInterrupt as err:
                print('Interrupt at ' + self.component_name + ' :\n' + err.args[0])

    def signal(self, message):
        pass

    def listen(self):
        while self.is_lock or len(self.buffer) == 0:
            continue
        res = self.buffer[0]
        self.buffer = self.buffer[1:]
        return res
    
    def lock(self):
        self.is_lock = True

    def unlock(self):
        self.is_lock = False
   
    def flush(self):
        self.buffer = []

    def read_line(self, time_out = 10):
        line = []
        max_len_line = 128
        while True:
            char = self.listen()
            if char == '#':
                return str.join('', line)
            line.append(char)
            if len(line) ==  max_len_line:
                return str.join('', line)
    



#row_pins = [17, 27, 22, 5]
#row_pins = [11, 13, 15, 29]
#col_pins = [23, 19, 26, 16]
#col_pins = [16, 35, 37, 36]
#keypad = Keypad(row_pins, col_pins)
#time.sleep(10)

#while True:
    #val = keypad.listen()
    #print(val)


