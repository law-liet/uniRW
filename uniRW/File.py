from __future__ import absolute_import
from os.path import isfile
from uniRW.Line import Line, OutputLine
from copy import copy

class File:

    def __init__(self, file_name, line):
        self.file_name = file_name
        self.line = copy(line)


class DataFile(File):

    def __init__(self, file_name, line, header_lineno=-1):
        if not isinstance(line, Line):
            raise ValueError("line is not a Line object.")
        File.__init__(self, file_name, line)
        if not isfile(file_name):
            raise ValueError(str(file_name) +" is not a file or not found")
        self.header_lineno = header_lineno
        self.__init_line = copy(line)

    def reset(self):
        self.line = copy(self.__init_line)

class OutputFile(File):

    def __init__(self, file_name, line, header=[], foreword=[], epilogue=[]):
        if not isinstance(line, OutputLine):
            raise ValueError("line is not a Line object.")
        File.__init__(self, file_name, line)
        self.header = copy(header)
        self.foreword = copy(foreword)
        self.epilogue = copy(epilogue)