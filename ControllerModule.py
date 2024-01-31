from ErrorHandlerModule import ErrorHandler
from LCDModule import LCD
from KeypadModule import Keypad
from ServiceHandlerModule import ServiceHandler
from RFIDModule import RFIDReader
from AuthenticatorModule import Authenticator
import threading
class Controller:
    def __init__(self):
        self.lcd = LCD()
        #self.rfid_reader = RFIDReader()
        self.rfid_reader = None
        self.row_pins = [17, 27, 22, 5]
        #self.row_pins = [11, 13, 15, 29]
        self.col_pins = [23, 19, 26, 16]
        #self.col_pins = [16, 35, 37, 36]
        self.input = Keypad(self.row_pins, self.col_pins)
        #self.error_handler = ErrorHandler(18, 20, 21, 12, self.lcd)
        #self.service_handler = ServiceHandler(0, self.input, self.lcd)
        self.authenticator = Authenticator(self.input, self.lcd, self.rfid_reader)

    def shutdown(self):
        exit(1)

    def run_error_handler(self):
        error_condvar = threading.Event()
        error_handled_condvar = threading.Event()

        self.error_handler.set_event(error_condvar, error_handled_condvar)
        self.error_handler.start()


        while True:
            error_condvar.wait()
            error_condvar.clear()
            self.keypad.lock()
            self.rfid_reader.lock()
            error_handled_condvar.wait(10)

            if error_handled_condvar.is_set():
                error_handled_condvar.clear()
                self.keypad.unlock()
                self.rfid_reader.unlock()
                continue
            else:
                self.shutdown()
        
    def run_service_handler(self, client_id):
        self.service_handler.client_id = str(client_id)
        res = self.service_handler.run()

    def run(self):
        #thread_error_handler = thread.Thread(target=self.run_error_handler)
        #thread_error_handler.start()

        while True:
            client_id = self.authenticator.run()
            print(client_id)
            #self.service_handler(client_id)
            
controller =  Controller()
controller.run()




