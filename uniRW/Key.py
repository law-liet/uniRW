from __future__ import print_function
from .Util import idenR

class GeneralKey:

    def __init__(self, name, map_f, to_string):
        self.name = name
        self.map_f = map_f
        self.to_string = to_string

class Key(GeneralKey):

     def __init__(self, column, name, map_f=idenR, to_string=str):
         GeneralKey.__init__(self, name, map_f, to_string)
         self.column = column

class StateKey(GeneralKey):

    def __init__(self, state_name, name, map_f=idenR, to_string=str):
        GeneralKey.__init__(self, name, map_f, to_string)
        self.state_name = state_name

