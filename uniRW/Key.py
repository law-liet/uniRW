from __future__ import print_function
from .util import idenR

class GeneralKey:

    def __init__(self, name, map_f, to_string):
        self.name = name
        self.map_f = map_f
        self.to_string = to_string

class Key(GeneralKey):

     def __init__(self, name, map_f=idenR, to_string=str):
         GeneralKey.__init__(self, name, map_f, to_string)


class StateKey(GeneralKey):

    def __init__(self, name, map_f=idenR, to_string=str):
        GeneralKey.__init__(self, name, map_f, to_string)


