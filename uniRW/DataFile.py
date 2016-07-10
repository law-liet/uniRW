class File:

    def __init__(self, file_name, split_by):
        self.filename = file_name
        self.split_by = split_by

class DataFile(File):

    def __init__(self, file_name, split_re, has_header=False, skip_chars=[]):
        File.__init__(self, file_name, split_re)
        self.has_header = has_header
        self.skip_chars = []

class OutputFile(File):

    def __init__(self, file_name, split_char, *, header=[], foreword=[], epilogue=[], end_char='\n'):
        File.__init__(self, file_name, split_char)
        self.header = []
        self.foreword = foreword
        self.epilogue = epilogue
        self.end_char = end_char