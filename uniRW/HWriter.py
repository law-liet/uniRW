from __future__ import absolute_import, print_function

from uniRW.Value import GeneralValue
from uniRW.Hierarchy import Hierarchy


class HWriter:

    def __init__(self, hierarchy_spec, value_line):
        """Initialize the writer.

        :param hierarchy_spec: a hierarchy specification (described in Hierarchy.py) describing the input dictionary.
        :param value_line ([GeneralValue]): an ordered value object list specifying each line of output.
        """
        Hierarchy.check(hierarchy_spec)
        for value in value_line:
            if not isinstance(value, GeneralValue):
                raise ValueError("Value is not a value object")

        self.hierarchy_spec = hierarchy_spec
        self.value_line = value_line

    def write(self, out_file, value_hierarchy, mode='w', sort_by=None, reverse=False):
        """Write a file according to value line specification.

        :param out_file (OutputFile): the file to write
        :param value_hierarchy (dict): a value hierarchy (dictionary) for writing to the file
        :param mode (str): writing mode ("w", "w+", ...)
        :param sort_by (str): the name of a value to sort by
        :param reverse: sort in reverse order or not
        """
        output = open(out_file.file_name, mode)

        # print foreword
        for foreword_line in out_file.foreword:
            print(foreword_line, file=output)

        # print header
        if out_file.header != []:
            header_line = out_file.line.get_line(out_file.header)
        else:
            header_line = out_file.line.get_line([value.name for value in self.value_line])
        print(header_line, file=output, end='')

        value_lines = []

        # flatten the value hierarchy (dictionary)
        Hierarchy.flatten(self.hierarchy_spec, value_hierarchy, value_lines)

        # sort the lines
        if sort_by == None:
            sorted_lines = value_lines
        else:
            sorted_lines = sorted(value_lines, key= lambda v_dict: v_dict[sort_by], reverse= reverse)

        # print value with respect to value line specification
        for line in sorted_lines:
            values = []
            for value in self.value_line:
                values.append(value.to_string(line[value.name]))
            print(out_file.line.get_line(values), file=output, end='')

        # print the epilogue
        for epilogue_line in out_file.epilogue:
            print(epilogue_line, file=output)

        output.close()
