from uniRW.Value import Value, StateValue
from uniRW.State import State
from uniRW.File import DataFile
from copy import copy

class HReader:

    def __init__(self, hierarchy, state=None, filter_f=lambda _,x: True):
        self.hierarchy = hierarchy
        self.state = state
        self.filter_f = filter_f


    def apply_post_map(self, layer, state, value_hierarchy):
        if type(layer) is list:

            for value in layer:
                if isinstance(value, StateValue):
                    val_name = value.name
                    if state.check(val_name):
                        val = value.post_map_f(state, value_hierarchy[val_name])
                    else:
                        raise KeyError(str(value.name) + " is not in state")
                elif isinstance(value, Value):
                    val_name = value.name
                    val = value.post_map_f(state, value_hierarchy[val_name])
                else:
                    raise ValueError("Value is not a Value or StateValue object")

                value_hierarchy[val_name] = val

        elif type(layer) is dict:
            value, next_layer = layer.items()[0]
            for val_name, _ in value_hierarchy.items():
                self.apply_post_map(next_layer, state, value_hierarchy[value.name])
        else:
            raise ValueError("Invalid hierarchy structure")



    def merge(self, layer, value_hierarchy1, value_hierarchy2, post=False, state=None):
        merged_hierarchy = value_hierarchy1.copy()

        if type(layer) is list:

            for value in layer:
                val1 = value_hierarchy1[value.name]
                val2 = value_hierarchy2[value.name]
                if post:
                    new_val1 = value.post_map_f(state, val1)
                    new_val2 = value.post_map_f(state, val2)
                    new_val = value.post_reduce_f(new_val1, new_val2)
                else:
                    new_val = value.reduce_f(val1,val2)
                merged_hierarchy[value.name] = new_val

        elif type(layer) is dict:
            value, next_layer = layer.items()[0]
            for val, next_val_layer2 in value_hierarchy2.items():
                if val in value_hierarchy1:
                    next_val_layer1 = value_hierarchy1[val]
                    merged_hierarchy[val] = self.merge(next_layer, next_val_layer1, next_val_layer2)
                else:
                    merged_hierarchy[val] = self.apply_post_map(next_layer, state, next_val_layer2)
        else:
            raise ValueError("Invalid hierarchy structure")

        return merged_hierarchy


    def traverse(self, layer, data_file, current_state, value_hierarchy):

        if type(layer) is list:

            for value in layer:

                if isinstance(value, StateValue):
                    val_name = value.name
                    if current_state.check(val_name):
                        val = value.map_f(current_state, current_state.get(val_name))
                    else:
                        raise KeyError(str(value.name) + " is not in state")
                elif isinstance(value, Value):
                    val_name = value.name
                    val = value.map_f(current_state, data_file.line.get_by_name(val_name))
                else:
                    raise ValueError("Value is not a Value or StateValue object")

                if val_name in value_hierarchy:
                    current_val = value_hierarchy[val_name]
                    reduced_val = value.reduce_f(current_val, val)
                    value_hierarchy[val_name] = reduced_val
                else:
                    value_hierarchy[val_name] = val

        elif type(layer) is dict:

            value, next_layer = layer.items()[0]

            if isinstance(value, StateValue):
                val_name = value.name
                if current_state.check(val_name):
                    val = value.map_f(current_state, current_state.get(val_name))
                else:
                    raise KeyError(str(value.name) + " is not in state")
            elif isinstance(value, Value):
                val_name = value.name
                val = value.map_f(current_state, data_file.line.get_by_name(val_name))
            else:
                raise ValueError("Value is not a Value or StateValue object")

            if val in value_hierarchy:
                new_hierarchy = {}
                self.traverse(next_layer, data_file, current_state, new_hierarchy)
                current_hierarchy = value_hierarchy[val]
                merged_hierarchy = self.merge(next_layer, current_hierarchy, new_hierarchy)
                value_hierarchy[val] = merged_hierarchy

            else:
                value_hierarchy[val] = {}
                self.traverse(next_layer, data_file, current_state, value_hierarchy[val])

        else:
            raise ValueError("Invalid hierarchy structure")


    def read(self, data_file, mode='r', apply_post_map=False, carry_state=False):

        if not isinstance(data_file, DataFile):
            raise ValueError("Data file is not a DataFile object.")

        lineno = 0
        value_hierarchy = {}
        current_state = None
        if self.state != None:
            if not isinstance(self.state, State):
                raise ValueError("State is a State object")

            if not carry_state:
                current_state = copy(self.state)
            else:
                current_state = self.state

        with open(data_file.file_name, mode) as file:

             for line in file:

                data_file.line.set(line[:-1])

                if data_file.header_lineno == lineno:
                    data_file.line.set_header()
                    lineno += 1
                    continue

                if self.state != None:
                    current_state.release()
                    current_state.update(data_file.line)
                    current_state.lock()

                if not self.filter_f(current_state, data_file.line):
                    lineno += 1
                    continue

                self.traverse(self.hierarchy, data_file, current_state, value_hierarchy)

                lineno += 1

        if apply_post_map:
            self.apply_post_map(self.hierarchy,current_state,value_hierarchy)

        return value_hierarchy, current_state


    def readAll(self, data_files, mode='r', carry_state=False):

        final_value_hierarchy = {}

        for data_file in data_files:
            value_hierarchy, final_state = self.read(data_file= data_file, mode=mode)
            final_value_hierarchy = \
                self.merge(self.hierarchy, final_value_hierarchy, value_hierarchy, True, final_state)

        return final_value_hierarchy