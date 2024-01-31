from Components import *
import time
import threading
from Client import *


class ServiceHandler:
    MENU = ['A', 'B', 'C', 'D', '*']
    VALID_CHAR = [str(i) for i in range(0, 10)]

    ACTION_MAP = {'A': 'CHANGE PASS', 'B': 'SHOW ASSET', 'C': 'LAST TRANSACTION', 'D': 'TRANSACTION', '*': 'Quit'}

    def __init__(self, client_id, input_: Component, output: Component):
        self.client_id = client_id
        self.input = input_
        self.output = output

    def get_user_password(self):
        
        return 'self.ki'

    def post_user_transaction(self, transaction, dest):
        server = Client()
        a, b, c = server.get_user_info(self.client_id)
        
        amount = None
        if dest == self.client_id:
            amount = 'A' + str(transaction)
        else:
            if int(transaction) > int(a):
                return None
            amount = 'B' + str(transaction)

        server = Client()
        server.update_user_amount(self.client_id, amount)
        
        return a

    def post_user_new_password(self, new_pass):
        server = Client()
        a, b, c = server.update_user_password(self.client_id, str(new_password))
        return a

    def get_user_assets(self):
        server = Client()
        a, b, c = server.get_user_info(self.client)
        return a

    def get_user_last_transaction(self):
        server = Client()
        a, b, c = server.get_user_info(self.client)
        return c

    def read_int(self, show_input=True):
        int_buffer = []
        int_max_len = 16
        self.input.flush()
        while True:
            char = self.input.listen()
            if char == '#':
                self.print('', 2)
                return str.join('', int_buffer)
            if char == '*':
                int_buffer.pop()
                if show_input:
                    self.print(str.join('', int_buffer), 2)
                continue

            print(char == '1')
            if char not in ServiceHandler.VALID_CHAR:
                return None

            if len(int_buffer) == int_max_len:
                self.print('', 2)
                return None

            int_buffer.append(char)
            if show_input:
                self.print(str.join('', int_buffer), 2)

    def read_password(self):
        return self.read_int(False)

    def print(self, message_str, line=1):
        message = Message(message_str, {'line': line})
        self.output.signal(message)
        time.sleep(0.1)

    def authenticate_password(self):
        password = self.read_password()
        if password is None:
            self.print('BAD PASS!')
            self.print('', 2)
            return False
        user_pass = self.get_user_password()
        if password != user_pass:
            self.print('WRONG PASS!')
            self.print('', 2)
            return False
        return True

    def wait_on_menu(self):
        _ = self.input.listen()
        self.print('')
        self.print('', 2)

    def change_pass(self):
        self.print('ENTER PASS')
        password = self.read_password()
        if password is None:
            self.print('BAD PASS!', 2)
            self.wait_on_menu()
            return
        res = self.post_user_new_password(password)
        if res is None:
            self.print('Error!', 2)
        else:
            self.print('Done!', 2)
        self.wait_on_menu()

    def show_asset(self):
        self.print('YOUR ASSETS:')
        assets = self.get_user_assets()
        self.print(assets, 2)
        self.wait_on_menu()

    def show_last_transaction(self):
        self.print('YOUR LAST TRN:')
        last_trn = self.get_user_last_transaction()
        if last_trn is None:
            self.print('No Transaction!', 2)
        else:
            self.print(last_trn, 2)
        self.wait_on_menu()
        
    def transaction(self):
        self.print('TYPE AMOUNT:')
        amount = self.read_int()
        if amount is None:
            self.print('Error!',2)
            self.wait_on_menu()
            return

        self.print('TYPE DST:')
        destination_id = self.read_int()
        if destination_id is None:
            self.print('Error!',2)
            self.wait_on_menu()

        state = self.post_user_transaction(amount, destination_id)
        self.print('STATUS:')
        if state is None:
            self.print('Error!', 2)
        else:
            self.print('DONE!', 2)
        self.wait_on_menu()
        
    def quit(self):
        self.print('BYE BYE!')
        self.wait_on_menu()

    def run(self):
        if True:
            while True:
                self.print('SELECT MENU')
                menu = self.input.listen()

                if menu not in ServiceHandler.MENU:
                    self.print('WRONG MENU!')
                    self.wait_on_menu()
                    continue
                else:
                    action = ServiceHandler.ACTION_MAP[menu]
                    if action == 'CHANGE PASS':
                        self.change_pass()
                    elif action == 'SHOW ASSET':
                        self.show_asset()
                    elif action == 'LAST TRANSACTION':
                        self.show_last_transaction()
                    elif action == 'TRANSACTION':
                        self.transaction()
                    else:
                        self.quit()
                        return 0
        return 1


#from LCDModule import LCD
#from KeypadModule import Keypad
#keypad = Keypad([17, 27, 22, 5], [23, 19, 26, 16])
#lcd = LCD()
#handler = ServiceHandler(0, keypad, lcd)
#
#while True:
#    handler.run()
