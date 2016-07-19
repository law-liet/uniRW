from __future__ import print_function
from __future__ import absolute_import
from uniRW.util import idenR

class GeneralValue:

    def __init__(self, name, to_string, map_f, reduce_f, post_map_f, post_reduce_f):
        self.name = name
        self.map_f = map_f
        self.reduce_f = reduce_f
        self.to_string = to_string
        self.post_map_f = post_map_f
        self.post_reduce_f = post_reduce_f


class Value(GeneralValue):

    def __init__(self, name, to_string=str, map_f=idenR,
                 reduce_f=idenR, post_map_f=idenR, post_reduce_f=idenR):
        GeneralValue.__init__(self, name, to_string, map_f, reduce_f, post_map_f, post_reduce_f)


class StateValue(GeneralValue):

    def __init__(self, name, to_string=str, map_f=idenR,
                 reduce_f=idenR, post_map_f=idenR, post_reduce_f=idenR):
        GeneralValue.__init__(self, name, to_string,  map_f, reduce_f, post_map_f, post_reduce_f)
