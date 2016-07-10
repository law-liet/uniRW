from __future__ import print_function
from .Util import idenR

class GeneralValue:

    def __init__(self, name, map_f=idenR, reduce_f=idenR):
        self.name = name
        self.map_f = map_f
        self.reduce_f = reduce_f


class Value(GeneralValue):

    def __init__(self, name, column, map_f=idenR, reduce_f=idenR):
        GeneralValue.__init__(name, map_f, reduce_f)
        self.column = column

class StateValue(GeneralValue):

    def __init__(self, name, state_name, map_f=idenR, reduce_f=idenR):
        GeneralValue.__init__(name, map_f, reduce_f)
        self.state_name = state_name