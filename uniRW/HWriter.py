from __future__ import print_function

from uniRW.Value import GeneralValue
from uniRW.Hierarchy import Hierarchy

class HWriter:

    def __init__(self, hierarchy_spec, value_line):
        Hierarchy.check(hierarchy_spec)
        self.hierarchy_spec = hierarchy_spec
        self.value_line = value_line

    def write(self, out_file, value_hierarchy, mode='w', sort_by=None, reverse=False):

        output = open(out_file.file_name, mode)
        for foreword_line in out_file.foreword:
            print(foreword_line, file=output)
        if out_file.header != []:
            header_line = out_file.line.get_line(out_file.header)
        else:
            header_line = out_file.line.get_line([value.name for value in self.value_line])
        print(header_line, file=output, end='')

        value_lines = []
        Hierarchy.flatten(self.hierarchy_spec, value_hierarchy, value_lines)
        if sort_by == None:
            sorted_lines = value_lines
        else:
            sorted_lines = sorted(value_lines, key= lambda v_dict: v_dict[sort_by], reverse= reverse)

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
