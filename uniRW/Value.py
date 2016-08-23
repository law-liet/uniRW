from __future__ import absolute_import

from uniRW.util import idenR


class GeneralValue:

    def __init__(self, name, to_string, map_f, reduce_f, post_map_f, post_reduce_f):
        """Initialize a value structure defining what and how to read and write

        :param name (str): the name (column name in header, or name of a state variable) of a value.
        :param to_string ('a -> str): a function turning a value to string for printing.
        :param map_f (State * 'a -> 'b): a function transforming a value (with access to state) during reading.
        :param reduce_f ('b * 'b -> 'b): an associative function reducing two values into one during reading.
        :param post_map_f (State * 'a -> 'b): a function transforming a value (with access to state) after reading.
        :param post_reduce_f ('b * 'b -> 'b): an associative function reducing two values into one after reading.
        """
        self.name = name
        self.map_f = map_f
        self.reduce_f = reduce_f
        self.to_string = to_string
        self.post_map_f = post_map_f
        self.post_reduce_f = post_reduce_f


class Value(GeneralValue):

    def __init__(self, name, to_string=str, map_f=idenR,
                 reduce_f=idenR, post_map_f=idenR, post_reduce_f=idenR):
        """Initialize a value from a line
        Subclass of GeneralValue with default input.
        """
        GeneralValue.__init__(self, name, to_string, map_f, reduce_f, post_map_f, post_reduce_f)

    def state_value(self):
        return StateValue(self.name, self.to_string, self.map_f, self.reduce_f, self.post_map_f, self.post_reduce_f)


class StateValue(GeneralValue):

    def __init__(self, name, to_string=str, map_f=idenR,
                 reduce_f=idenR, post_map_f=idenR, post_reduce_f=idenR):
        """Initialize a value from state
        Subclass of GeneralValue with default input.
        """
        GeneralValue.__init__(self, name, to_string,  map_f, reduce_f, post_map_f, post_reduce_f)

    def value(self):
        return Value(self.name, self.to_string, self.map_f, self.reduce_f, self.post_map_f, self.post_reduce_f)
