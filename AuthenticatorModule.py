from Components import *
from KeypadModule import Keypad
from LCDModule import LCD
from Client import *
import time
import threading
from RFIDModule import RFIDReader


class Authenticator:

    def __init__(self, keypad, lcd, rfid):
        super().__init__()
        self.lcd = lcd
        self.keypad = keypad
        self.rfid = rfid
        self.user_id = None

    def empty_input(self):
        message = Message('', {"line": 2})
        self.keypad.flush()
        self.lcd.signal(message)

    def print_error(self, text):
        self.print_info(text)
        time.sleep(2)

    def print_info(self, text):
        self.empty_input()
        message = Message(text, {'line': 1})
        self.lcd.signal(message)
        time.sleep(1)

    def receive_command(self):
        message = Message('', {"line":1})
        input_buffer = []
        while True:
            c = str(self.keypad.listen())
            if c == '*':
                input_buffer.pop()
            elif c == '#':
                break
            else:
                input_buffer.append(c)
            message.content = str.join('', input_buffer)
            message.meta_data['line'] = 2
            self.lcd.signal(message)
            time.sleep(1)
        return str.join('', input_buffer)

    def get_password_from_server(self, user_id):
        server = Client()
        amount, user_password = server.get_user_info(user_id)
        return user_password

    def check_the_password(self, card_id):
        self.print_info('Input password:')
        password = self.receive_command()
        user_password = self.get_password_from_server(card_id)
        if password == user_password:
            self.user_id = card_id
        else:
            self.print_error('Incorrect pass!')

    def log_in_with_tag_handler(self):
        self.print_info('Bring the tag')
        card_id = self.rfid.listen()
        if card_id == '878964088224':
            self.check_the_password(card_id)
        else:
            self.print_error('Wrong Tag!')

    def get_user_by_phrases(self, phrases):
        server = Client()
        a, b, c = server.get_user_id_by_phrases(phrases)
        self.user_id = str(a)

    def log_in_with_12_phrases(self):
        self.print_info('Enter 12 phrase')
        phrases = []
        for i in range(12):
            phrase = self.receive_command()
            phrases.append(phrase)
        s = str.join('#', phrases)

    def run(self):
        while True:
            self.print_info('A-Tag B-12_phr')
            command = self.receive_command()
            if command == 'A':
                self.log_in_with_tag_handler()
            elif command == 'B':
                self.log_in_with_12_phrases()
            else:
                self.print_error('Wrong input!')

            if self.user_id:
                return self.user_id

