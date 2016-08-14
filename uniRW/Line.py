from re import split as split


class Line:

    def __init__(self, delimiter, name_col_dict={}):
        """Initialize a line object for reading.

        :param delimiter (str): a regular expression that splits a raw data line.
        :param name_col_dict: a dictionary (name => column) that maps value name to column number.
        """
        self.name_col_dict = name_col_dict.copy()
        self.delimiter = delimiter
        self.__line = []

    def get_by_name(self, name):
        if name in self.name_col_dict:
            return self.__line[self.name_col_dict[name]]
        else:
            raise KeyError(str(name) + " is not in a data line")

    def get_by_index(self, index):
        return self.__line[index]

    def store(self, line):
        """convert store a raw data line into a list and store it in the line object

        :param line (str): a raw data line
        """
        self.__line = split(self.delimiter, line)

    def set_header(self):
        """Make the name => column dictionary from current stored values by indexing.
        """
        for i, val in enumerate(self.__line):
            if val in self.name_col_dict:
                continue
            else:
                self.name_col_dict[val] = i

    def clear(self):
        self.name_col_dict = {}
        self.__line = []


class OutputLine:

    def __init__(self, delimiter, end_char='\n'):
        """Initialize a outputLine object for writing.

        :param delimiter (str): the delimiter of a line.
        :param end_char: the ending character of a line.
        """
        self.delimiter = delimiter
        self.end_char = end_char

    def get_line(self, values):
        """Join a list of strings by the delimiter

        :param values ([str]): a list of strings
        :return (str): the result string
        """
        return self.delimiter.join(values) + self.end_char
