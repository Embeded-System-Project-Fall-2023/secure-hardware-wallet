from Components import Message
from GasSensorModule import GasSensor
from BuzzerModule import Buzzer
from LEDModule import LED
from TempModule import TempSensor
from LCDModule import LCD
import threading
import time



class ErrorHandler(threading.Thread):
    TEMP_THRESHOLD = 75
    HUMID_THRESHOLD = 40

    def __init__(self, led_pin, buzzer_pin, temp_sens_pin, gas_sensor_pin, lcd_module):
        super().__init__()
        self.gas_sensor_pin = gas_sensor_pin
        self.led_pin = led_pin
        self.temp_sens_pin = temp_sens_pin
        self.buzzer_pin = buzzer_pin

        self.led = LED(led_pin)
        self.buzzer = Buzzer(buzzer_pin)
        self.temp_sensor = TempSensor(temp_sens_pin)
        self.gas_sensor = GasSensor(gas_sensor_pin)

        self.temp_situation = threading.Event()
        self.gas_situation = threading.Event()
        self.temp_situation.set()
        self.gas_situation.set()
        self.lcd = lcd_module
        self.error_activated = False
        self.prev_lcd_content = ['', '']


    def restore_lcd(self):
        message_1 = Message(self.prev_lcd_content[0], meta_data={'line': 1})
        message_2 = Message(self.prev_lcd_content[1], meta_data={'line': 2})
        self.lcd.signal(message_1)
        time.sleep(0.1)
        self.lcd.signal(message_2)

    def print_error_on_lcd(self):
        self.prev_lcd_content = self.lcd.last_message.copy()
        message_1 = Message('Bad situation', meta_data={'line': 1})
        message_2 = Message('Fix Quickly!', meta_data={'line': 2})
        self.lcd.signal(message_1)
        time.sleep(0.1)
        self.lcd.signal(message_2)

    def set_error_situation(self, situation):
        if situation == 'on': 
            self.error_activated = True
            self.print_error_on_lcd()
        else:
            self.error_activated = False
            self.restore_lcd()
        self.led.signal(Message(situation))
        self.buzzer.signal(Message(situation))

    def set_event(self, error_event: threading.Event, handled_event: threading.Event):
        self.error_event = error_event
        self.handled_event = handled_event

    def listen_for_error(self):
        print('Listening for Errors')
        is_off = True
        while True:
            if not self.gas_situation.is_set():
                self.gas_situation.wait(2)
                if not self.gas_situation.is_set():
                    if self.error_activated: continue
                    
                    is_off = False
                    self.error_event.set()
                    self.set_error_situation('on')
                    time.sleep(2)

            elif not self.temp_situation.is_set():
                self.temp_situation.wait(2)
                if not self.temp_situation.is_set():
                    if self.error_activated: continue
                    
                    is_off = False
                    self.error_event.set()
                    self.set_error_situation('on')
                    time.sleep(2)
            elif not is_off:
                is_off = True
                self.set_error_situation('off')
                self.handled_event.set()

    def temp_sens_listener(self):
        print('Temp Sensor Listener Activated')
        while True:
            temp, humidity = self.temp_sensor.listen()
            if temp > ErrorHandler.TEMP_THRESHOLD or humidity > ErrorHandler.HUMID_THRESHOLD:
                self.temp_situation.clear()
            else:
                self.temp_situation.set()
            time.sleep(0.5)

    def gas_sens_listener(self):
        print('Gas Detector Listener Activated')
        while True:
            state = self.gas_sensor.listen()
            if state == 0:
                self.gas_situation.clear()
            else:
                self.gas_situation.set()
            time.sleep(0.5)

    def run(self):
        print('Error Handler Activated')
        temp_listen_thread = threading.Thread(target=self.temp_sens_listener)
        gas_listen_thread = threading.Thread(target=self.gas_sens_listener)
        temp_listen_thread.start()
        gas_listen_thread.start()
        self.listen_for_error()


#lcd = LCD()
#error_event = threading.Event()
#handled_event = threading.Event()
#error_handler = ErrorHandler(18, 20, 21, 12, lcd)
#error_handler.set_event(error_event, handled_event)
#error_handler.start()
