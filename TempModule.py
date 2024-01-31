from Components import *
import Adafruit_DHT as dht
import time
import threading


class TempSensor(Component):
    def __init__(self, pin_id):
        super().__init__('Temp Sensor')
        self.pin_id = pin_id
        self.temp = None
        self.humidity = None
        self.last_update = None
        self.cond_var.set()
        self.cond_var_support_lock.release()

    def active_mode(self):
        print('In Active Mode ' + self.component_name)
        while True:
            try:
                self.temp, self.humidity = dht.read_retry(dht.DHT22, self.pin_id)
                time.sleep(0.25)
                self.last_update = time.time_ns()
            except RuntimeError as err:
                print('Error at ' + self.component_name + ' :\n' + err.args[0])

    def signal(self, message):
        pass

    def listen(self):
        # now = time.time_ns()
        # while (self.last_update - now) > 500_000_000:
        #     continue

        if None in [self.temp, self.humidity]:
            while None in [self.temp, self.humidity]:
                continue

        return self.temp, self.humidity


#temp_sensor = TempSensor(21)
#while True:
#    t, h = temp_sensor.listen()
#    print(f'Temp: {t}, Humidity: {h}')
#    time.sleep(5)

