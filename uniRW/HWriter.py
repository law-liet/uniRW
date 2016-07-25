from __future__ import print_function
from uniRW.Value import GeneralValue

class HWriter:

    def __init__(self, hierarchy_spec, value_line=[]):
        self.hierarchy_spec = hierarchy_spec
        self.value_line = value_line

    def flatten(self, layer, value_hierarchy, value_lines, value_line={}):

        for root, next in value_hierarchy.items():

            if type(layer) is list:
                current_value_line = value_line
                for value in layer:
                    if isinstance(value, GeneralValue):
                        current_value_line[value.name] = value_hierarchy[value.name]
                    else:
                        val, next_layer = value
                        self.flatten(next_layer, next, value_lines, current_value_line)

            elif type(layer) is dict:
                current_value_line = value_line.copy()
                value, next_layer = layer.items()[0]
                current_value_line[value.name] = root
                self.flatten(next_layer, next, value_lines, current_value_line)
                value_lines.append(current_value_line)

            else:
                current_value_line = value_line
                val, next_layer = layer
                self.flatten(next_layer, next, value_lines, current_value_line)


    def write(self, out_file, value_hierarchy, mode='w', sort_by=None, reverse=False):

        output = open(out_file.file_name, mode)
        for foreword_line in out_file.foreword:
            print(foreword_line, file=output)
        if out_file.header != []:
            header_line = out_file.line.get_line(out_file.header)
            print(header_line, file=output, end='')

        value_lines = []
        self.flatten(self.hierarchy_spec, value_hierarchy, value_lines)
        sorted_lines = sorted(value_lines, key=lambda v_dict: v_dict[sort_by])

        for line in sorted_lines:
            values = []
            for value in self.value_line:
                if isinstance(value, GeneralValue):
                    values.append(value.to_string(line[value.name]))
                else:
                    raise ValueError("Value is not a value object")
            print(out_file.line.get_line(values), file=output, end='')

        for epilogue_line in out_file.epilogue:
            print(epilogue_line, file=output)

        output.close()
