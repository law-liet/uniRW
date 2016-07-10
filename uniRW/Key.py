from __future__ import print_function
from .Util import idenR
import sys

class Key:

    def __init__(self, column, name, map_f=idenR):
        self.column = column
        self.name = name
        self.map_f = map_f