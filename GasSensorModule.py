from Components import *
import time
import threading
import RPi.GPIO as GPIO



class GasSensor(Component):
    def __init__(self, pin_id):
        super().__init__('Gas Sensor')
        self.pin_id = pin_id
        self.__init_pins()
        self.last_read = None
        self.last_update = None
        self.cond_var.set()
        self.cond_var_support_lock.release()

    def __init_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_id, GPIO.IN)

    def active_mode(self):
        print('In Active Mode ' + self.component_name)
        while True:
            try:
                self.last_read = GPIO.input(self.pin_id)
                time.sleep(0.25)
                self.last_update = time.time_ns()
            except RuntimeError as err:
                print('Error at ' + self.component_name + ' :\n' + err.args[0])

    def signal(self, message):
        pass

    def listen(self):
        while self.last_read is None:
            continue
        return self.last_read


#gas_sensor = GasSensor(12)
#while True:
#    print(gas_sensor.listen())
#    time.sleep(2)

