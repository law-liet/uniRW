from re import split as resplit

class Line:

    def __init__(self, delimiter, name_col_dict={}):
        self.name_col_dict = name_col_dict
        self.delimiter = delimiter
        self.__line = None

    def get_by_name(self, name):
        if name in self.name_col_dict:
            return self.__line[self.name_col_dict[name]]
        else:
            raise KeyError(str(name) + " is not in a data line")

    def get_by_index(self, index):
        return self.__line[index]

    def set(self, line):
        self.__line = resplit(self.delimiter, line)

    def set_header(self):
        for i,val in enumerate(self.__line):
            if val in self.name_col_dict:
                continue
            else:
                self.name_col_dict[val] = i

class OutputLine:

    def __init__(self, delimiter, end_char='\n'):
        self.delimiter = delimiter
        self.end_char = end_char

    def get_line(self, values):
        return self.delimiter.join(values) + self.end_char