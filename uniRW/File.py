from os.path import isfile

class File:

    def __init__(self, file_name, split_by):
        if isfile(file_name):
            self.file_name = file_name
        else:
            raise ValueError(str(file_name) +" is not a file or not found")
        self.split_by = split_by


class DataFile(File):

    def __init__(self, file_name, split_re):
        File.__init__(self, file_name, split_re)


class OutputFile(File):

    def __init__(self, file_name, split_char, *, header=[], foreword=[], epilogue=[], end_char='\n'):
        File.__init__(self, file_name, split_char)
        self.header = []
        self.foreword = foreword
        self.epilogue = epilogue
        self.end_char = end_char