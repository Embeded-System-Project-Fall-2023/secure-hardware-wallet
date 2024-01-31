import time
import threading

class Component:
    def __init__(self, name):
        self.component_name = name
        self.__init_thread()

    def __init_thread(self):
        self.cond_var_support_lock = threading.Lock()
        self.cond_var = threading.Event()
        self.cond_var.clear()
        self.main_thread = threading.Thread(target=self.run_component)
        self.cond_var_support_lock.acquire()
        self.main_thread.start()

    def idle_mode(self):
        print('In Idle Mode at ' + self.component_name)
        while True:
            self.cond_var.wait()
            if not self.cond_var_support_lock.locked():
                print('Exiting Idle Mode at ' + self.component_name)
                return

    def run_component(self):
        while True:
            self.idle_mode()
            self.cond_var.clear()
            self.active_mode()

    def active_mode(self):
        pass

    def listen(self):
        pass

    def signal(self, Message):
        pass

    def lock(self):
        return

    def unlock(self):
        return

class Message:
    def __init__(self, content=None, meta_data=None):
        self.content = content
        self.meta_data = meta_data


