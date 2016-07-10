

class Reader:

    def __init__(self, data_file, key, value, state, filter_f=lambda x:True):
        self.data_file = data_file
        self.key = key
        self.value = value
        self.state = state
        self.filter_f = filter_f

    def read(self, mode):
        pass

    def readAll(self, mode):
        pass