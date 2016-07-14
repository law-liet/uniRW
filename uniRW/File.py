from os.path import isfile

class File:

    def __init__(self, file_name, line):
        if isfile(file_name):
            self.file_name = file_name
        else:
            raise ValueError(str(file_name) +" is not a file or not found")
        self.line = line

class DataFile(File):

    def __init__(self, file_name, line, has_header=False):
        File.__init__(self, file_name, line)
        self.has_header = has_header

class OutputFile(File):

    def __init__(self, file_name, line, header=[], foreword=[], epilogue=[]):
        File.__init__(self, file_name, line)
        self.header = header
        self.foreword = foreword
        self.epilogue = epilogue