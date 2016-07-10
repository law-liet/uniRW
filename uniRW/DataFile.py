class DataFile:

    def __init__(self, file_name, split_re, has_header=False, skip_chars=[]):
        self.filename = file_name
        self.split_re = split_re
        self.has_header = has_header
        self.skip_chars = []