from re import split as split


class Line:

    def __init__(self, delimiter, name_col_dict={}):
        """Initialize a line object for reading.

        :param delimiter (str): a regular expression that splits a raw data line.
        :param name_col_dict (dict): a dictionary (name => column) that maps value name to column number.
        """
        self.name_col_dict = name_col_dict.copy()
        self.delimiter = delimiter
        self.__line = []

    def __getitem__(self, item):
        if type(item) is int:
            return self.get_by_index(item)
        else:
            return self.get_by_name(item)

    def __contains__(self, name):
        return name in self.name_col_dict

    def get_by_name(self, name):
        name_col_dict = self.name_col_dict
        if name in name_col_dict:
            return self.__line[name_col_dict[name]]
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
        name_col_dict = self.name_col_dict
        for i, val in enumerate(self.__line):
            if val in name_col_dict:
                continue
            else:
                name_col_dict[val] = i

    def clear(self):
        self.name_col_dict = {}
        self.__line = []


class OutputLine:

    def __init__(self, delimiter, start_char='', end_char='\n'):
        """Initialize a outputLine object for writing.

        :param delimiter (str): the delimiter of a line.
        :param end_char: the ending character of a line.
        """
        self.delimiter = delimiter
        self.start_char = start_char
        self.end_char = end_char

    def get_line(self, values):
        """Join a list of strings by the delimiter

        :param values ([str]): a list of strings
        :return (str): the result string
        """
        return self.start_char + self.delimiter.join(values) + self.end_char
