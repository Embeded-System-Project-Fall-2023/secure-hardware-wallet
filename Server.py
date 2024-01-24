# import RPi.GPIO as GPIO
# import SimpleMFRC522


class User:
    def init(self):
        pass


class Message:
    def init(self):
        pass


class Server:
    def init(self):
        pass


class Component:
    def init(self):
        pass

    def listen(self, deadline):
        pass

    def signal(self, message):
        pass


class Keypad(Component):
    def init(self):
        super().init()


class RFidReader(Component):
    def __init__(self, reader):
        super().init()
        self.reader = reader

    def listen(self, deadline):
        pass
