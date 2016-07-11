from re import split as resplit

class Line:

    def __init__(self, name_col_dict, split_by, line=None):
        self.name_col_dict = name_col_dict
        self.split_by = split_by
        if line == None:
            self.__line = None
        else:
            self.__line = resplit(self.split_by, line)

    def get(self, name):
        if self.__line == None:
            raise ValueError("Line is not yet set.")
        if name in self.name_col_dict:
            return self.__line[self.name_col_dict[name]]
        else:
            raise KeyError(str(name) + " is not in a data line")

    def set(self, line):
        self.__line = resplit(self.split_by, line)

class OuputLine:

    def __init__(self, split_char, end_char='\n'):
        self.split_by = split_char
        self.end_char = end_char

    def get_line(self, values):
        return self.split_by.join(values) + self.end_char