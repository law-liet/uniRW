from uniRW.Value import GeneralValue, Value, StateValue
from uniRW.State import State


class Hierarchy:

    @classmethod
    def check(cls, hierarchy):
        try:
            if type(hierarchy) is list:
                for value in hierarchy:
                    if not isinstance(value, GeneralValue):
                        _, next_layer = hierarchy
                        cls.check(next_layer)

            elif type(hierarchy) is dict:
                items = list(hierarchy.items())
                if len(items) != 1:
                    raise ValueError
                else:
                    _, next_layer = items[0]
                    cls.check(next_layer)
            else:
                _, next_layer = hierarchy
                cls.check(next_layer)
        except:
            print("Invalid hierarchy specification")
            raise

    @classmethod
    def apply_post_map(cls, layer, state, value_hierarchy):

        if type(layer) is list:

            for value in layer:
                if isinstance(value, GeneralValue):
                    val_name = value.name
                    val = value.post_map_f(state, value_hierarchy[val_name])
                    value_hierarchy[val_name] = val
                else:
                    val, next_layer = value
                    cls.apply_post_map(next_layer, state, value_hierarchy[val])

        elif type(layer) is dict:
            value, next_layer = list(layer.items())[0]
            for val, _ in value_hierarchy.items():
                cls.apply_post_map(next_layer, state, value_hierarchy[val])

        else:
            val, next_layer = layer
            cls.apply_post_map(next_layer, state, value_hierarchy[val])

    @classmethod
    def traverse(cls, layer, line, current_state, value_hierarchy):

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
                    cls.traverse(next_layer, line, current_state, value_hierarchy[val])

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
                cls.traverse(next_layer, line, current_state, value_hierarchy[val])

            if val in value_hierarchy:
                new_hierarchy = {}
                cls.traverse(next_layer, line, current_state, new_hierarchy)
                current_hierarchy = value_hierarchy[val]
                merged_hierarchy = cls.merge(next_layer, current_hierarchy, new_hierarchy)
                value_hierarchy[val] = merged_hierarchy

            else:
                value_hierarchy[val] = {}
                cls.traverse(next_layer, line, current_state, value_hierarchy[val])

        else:
            val, next_layer = layer
            value_hierarchy[val] = {}
            cls.traverse(next_layer, line, current_state, value_hierarchy[val])

    @classmethod
    def merge(cls, layer, value_hierarchy1, value_hierarchy2, post=False, state=State({})):
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
                        new_val = value.reduce_f(val1, val2)
                    merged_hierarchy[value.name] = new_val

                else:
                    val, next_layer = value
                    merged_hierarchy[val] = \
                        cls.merge(next_layer, value_hierarchy1[val], value_hierarchy2[val], post, state)

        elif type(layer) is dict:
            value, next_layer = list(layer.items())[0]
            for val, next_val_layer2 in value_hierarchy2.items():
                if val in value_hierarchy1:
                    next_val_layer1 = value_hierarchy1[val]
                    merged_hierarchy[val] = cls.merge(next_layer, next_val_layer1, next_val_layer2, post, state)
                else:
                    if post:
                        cls.apply_post_map(next_layer, state, next_val_layer2)
                    merged_hierarchy[val] = next_val_layer2

        else:
            val, next_layer = layer
            merged_hierarchy[val] = cls.merge(next_layer, value_hierarchy1[val], value_hierarchy2[val], post, state)

        return merged_hierarchy

    @classmethod
    def flatten(cls, layer, value_hierarchy, value_lines, value_line={}):

        for root, next in value_hierarchy.items():

            if type(layer) is list:
                current_value_line = value_line
                for value in layer:
                    if isinstance(value, GeneralValue):
                        current_value_line[value.name] = value_hierarchy[value.name]
                    else:
                        val, next_layer = value
                        cls.flatten(next_layer, next, value_lines, current_value_line)

            elif type(layer) is dict:
                current_value_line = value_line.copy()
                value, next_layer = list(layer.items())[0]
                current_value_line[value.name] = root
                cls.flatten(next_layer, next, value_lines, current_value_line)
                value_lines.append(current_value_line)

            else:
                current_value_line = value_line
                val, next_layer = layer
                cls.flatten(next_layer, next, value_lines, current_value_line)
