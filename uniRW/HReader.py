from uniRW.Value import Value, StateValue, GeneralValue
from uniRW.State import State
from uniRW.File import DataFile
from copy import copy

class HReader:

    def __init__(self, hierarchy_spec, state=None, filter_f=lambda _, x: True):
        self.hierarchy_spec = hierarchy_spec
        self.state = state
        self.filter_f = filter_f
        self.__init_state = copy(self.state)


    def apply_post_map(self, layer, state, value_hierarchy):
        if type(layer) is list:

            for value in layer:
                if isinstance(value, GeneralValue):
                    val_name = value.name
                    val = value.post_map_f(state, value_hierarchy[val_name])
                    value_hierarchy[val_name] = val
                else:
                    val, next_layer = value
                    self.apply_post_map(next_layer,state,value_hierarchy[val])


        elif type(layer) is dict:
            value, next_layer = list(layer.items())[0]
            for val, _ in value_hierarchy.items():
                self.apply_post_map(next_layer, state, value_hierarchy[val])
        else:
            val, next_layer = layer
            self.apply_post_map(next_layer,state,value_hierarchy[val])



    def merge(self, layer, value_hierarchy1, value_hierarchy2, post=False, state=None):
        merged_hierarchy = value_hierarchy1.copy()

        if type(layer) is list:

            for value in layer:

                if isinstance(value, GeneralValue):
                    val1 = value_hierarchy1[value.name]
                    val2 = value_hierarchy2[value.name]
                    if post:
                        new_val1 = value.post_map_f(state, val1)
                        new_val2 = value.post_map_f(state, val2)
                        new_val = value.post_reduce_f(new_val1, new_val2)
                    else:
                        new_val = value.reduce_f(val1,val2)
                    merged_hierarchy[value.name] = new_val

                else:
                    val, next_layer = value
                    merged_hierarchy[val] = \
                        self.merge(next_layer, value_hierarchy1[val], value_hierarchy2[val], post, state)

        elif type(layer) is dict:
            value, next_layer = list(layer.items())[0]
            for val, next_val_layer2 in value_hierarchy2.items():
                if val in value_hierarchy1:
                    next_val_layer1 = value_hierarchy1[val]
                    merged_hierarchy[val] = self.merge(next_layer, next_val_layer1, next_val_layer2, post, state)
                else:
                    if post:
                        self.apply_post_map(next_layer, state, next_val_layer2)
                    merged_hierarchy[val] = next_val_layer2
        else:
            val, next_layer = layer
            merged_hierarchy[val] = self.merge(next_layer, value_hierarchy1[val], value_hierarchy2[val], post, state)

            #raise ValueError("Invalid hierarchy_spec structure")

        return merged_hierarchy


    def traverse(self, layer, line, current_state, value_hierarchy):

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
                    val = value.map_f(current_state, line.get_by_name(val_name))
                else:
                    val, next_layer = value
                    value_hierarchy[val] = {}
                    self.traverse(next_layer, line, current_state, value_hierarchy[val])

                if val_name in value_hierarchy:
                    current_val = value_hierarchy[val_name]
                    reduced_val = value.reduce_f(current_val, val)
                    value_hierarchy[val_name] = reduced_val
                else:
                    value_hierarchy[val_name] = val

        elif type(layer) is dict:

            value, next_layer = list(layer.items())[0]

            if isinstance(value, StateValue):
                val_name = value.name
                if current_state.check(val_name):
                    val = value.map_f(current_state, current_state.get(val_name))
                else:
                    raise KeyError(str(value.name) + " is not in state")
            elif isinstance(value, Value):
                val_name = value.name
                val = value.map_f(current_state, line.get_by_name(val_name))
            else:
                val, next_layer = value
                value_hierarchy[val] = {}
                self.traverse(next_layer, line, current_state, value_hierarchy[val])

            if val in value_hierarchy:
                new_hierarchy = {}
                self.traverse(next_layer, line, current_state, new_hierarchy)
                current_hierarchy = value_hierarchy[val]
                merged_hierarchy = self.merge(next_layer, current_hierarchy, new_hierarchy)
                value_hierarchy[val] = merged_hierarchy

            else:
                value_hierarchy[val] = {}
                self.traverse(next_layer, line, current_state, value_hierarchy[val])

        else:
            val, next_layer = layer
            value_hierarchy[val] = {}
            self.traverse(next_layer, line, current_state, value_hierarchy[val])

            #raise ValueError("Invalid hierarchy_spec structure")


    def read(self, data_file, mode='r', apply_post_map=False, carry_state=False):

        if not isinstance(data_file, DataFile):
            raise ValueError("Data file is not a DataFile object.")

        lineno = 0
        value_hierarchy = {}
        value_hierarchy_list = []
        current_state = None

        if type(self.hierarchy_spec) is list:
            multi_hierarchy = True
        else:
            multi_hierarchy = False

        if self.state != None:
            if not isinstance(self.state, State):
                raise ValueError("State is a State object")

            if not carry_state:
                current_state = copy(self.state)
            else:
                current_state = self.state

        with open(data_file.file_name, mode) as file:

             for line in file:
                try:
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

                    if multi_hierarchy:
                        for i, hierarchy_spec in enumerate(self.hierarchy_spec):
                            if i >= len(value_hierarchy_list):
                                value_hierarchy_list.append(value_hierarchy.copy())
                            value_hierarchy_copy = value_hierarchy_list[i]
                            self.traverse(hierarchy_spec, data_file, current_state, value_hierarchy_copy)
                            value_hierarchy_list[i] = value_hierarchy_copy

                    else:
                        self.traverse(self.hierarchy_spec, data_file.line, current_state, value_hierarchy)

                except (KeyError, ValueError):
                    print("Error occurred when reading line" + str(lineno) + " of " + data_file.file_name)
                    raise

                lineno += 1

        if multi_hierarchy:

            if apply_post_map:
                for hierarchy_spec, value_hierarchy in zip(self.hierarchy_spec, value_hierarchy_list):
                    self.apply_post_map(hierarchy_spec, current_state, value_hierarchy)

            return value_hierarchy_list, current_state
        else:
            if apply_post_map:
                self.apply_post_map(self.hierarchy_spec, current_state, value_hierarchy)

            return value_hierarchy, current_state


    def readAll(self, data_files, mode='r', carry_state=False):

        if type(self.hierarchy_spec) is list:
            multi_hierarchy = True
        else:
            multi_hierarchy = False

        if multi_hierarchy:
            final_value_hierarchy_list = []

            for data_file in data_files:
                value_hierarchy_list, final_state = self.read(data_file, mode, carry_state)

                for i, value_hierarchy in enumerate(value_hierarchy_list):
                    if i >= len(final_value_hierarchy_list):
                        final_value_hierarchy_list.append({})
                    final_value_hierarchy = final_value_hierarchy_list[i]
                    final_value_hierarchy_list[i] = \
                        self.merge(self.hierarchy_spec[i], final_value_hierarchy, value_hierarchy, True, final_state)

            self.clear_state()
            return final_value_hierarchy_list

        else:
            final_value_hierarchy = {}

            for data_file in data_files:
                value_hierarchy, final_state = self.read(data_file, mode, carry_state)
                final_value_hierarchy = \
                    self.merge(self.hierarchy_spec, final_value_hierarchy, value_hierarchy, True, final_state)

            self.clear_state()
            return final_value_hierarchy

    def clear_state(self):
        self.state = copy(self.__init_state)