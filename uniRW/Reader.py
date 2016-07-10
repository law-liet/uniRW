

class Reader:

    def __init__(self, data_file, key, values, state, filter_f=lambda x:True):
        self.data_file = data_file
        self.key = key
        self.values = values
        self.state = state
        self.filter_f = filter_f

    def read(self, mode):
        pass

    def readAll(self, mode):
        pass
