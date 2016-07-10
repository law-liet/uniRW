from . import RW

class Reader:

    def __init__(self, key, value, state):
        self.key = key
        self.value = value
        self.state = state

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_state(self):
        return self.state

    def set_key(self, key):
        self.key = key

    def set_value(self, value):
        self.key = value

    def set_state(self, state):
        self.key = state

    def read(self, file_name, mode):
        pass

    def readAll(self, file_names, mode):
        pass