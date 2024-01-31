from Components import *
from mfrc522 import SimpleMFRC522



class RFIDReader(Component):
    def __init__(self):
        super().__init__('RFID Reader')
        self.reader = SimpleMFRC522()
        self.card_id = None
        self.data = None
        self.is_lock = False
        self.cond_var.set()
        self.cond_var_support_lock.release()


    def active_mode(self):
        return

    def signal(self, message):
        return

    def listen(self):
        while self.is_lock:
            continue
        self.card_id, self.data = self.reader.read()
        return self.card_id

    def lock(self):
        self.is_lock = True

    def unlock(self):
        self.is_lock = False
