from __future__ import absolute_import

from copy import copy
from os.path import isfile

from uniRW.Line import Line, OutputLine


class File:

    def __init__(self, file_name, line):
        """Initialize a file object.

        :param file_name (str): name.
        :param line (Line or OutputLine): a Line or OutputLine object describing a line in this file.
        """
        self.file_name = file_name
        self.line = copy(line)  # prevent bugs in sharing the same Line object


class DataFile(File):

    def __init__(self, file_name, line, header_lineno=-1):
        """Initialize a file object for reading.

        :param header_lineno (int): the line number (starting from 0) of the header of the file
        """
        if not isinstance(line, Line):
            raise ValueError("line is not a Line object.")
        File.__init__(self, file_name, line)
        if not isfile(file_name):
            raise ValueError(str(file_name) + " is not a file or not found")
        self.header_lineno = header_lineno
        self.__init_line = copy(line)  # private copy of line

    def reset(self):
        self.line = copy(self.__init_line)


class OutputFile(File):

    def __init__(self, file_name, line, header=[], foreword=[], epilogue=[]):
        """Initialize a file object for writing.

        :param header ([str]): the header of file.
        :param foreword ([str]): the foreword of a file with each string as a line.
        :param epilogue ([str]): the epilogue of a file with each string as a line.
        """
        if not isinstance(line, OutputLine):
            raise ValueError("line is not a OutputLine object.")
        File.__init__(self, file_name, line)
        self.header = copy(header)
        self.foreword = copy(foreword)
        self.epilogue = copy(epilogue)
