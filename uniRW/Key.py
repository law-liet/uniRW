from __future__ import print_function
from .Util import idenR

class Key:

    def __init__(self, column, name, map_f=idenR, to_string=str):
        self.column = column
        self.name = name
        self.map_f = map_f
        self.to_string = to_string
