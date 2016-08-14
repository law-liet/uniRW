from copy import copy

from uniRW.File import DataFile
from uniRW.State import State
from uniRW.Value import Value, StateValue, GeneralValue
from uniRW.Hierarchy import Hierarchy

class HReader:

    def __init__(self, hierarchy_spec, state=State({}), filter_f=lambda _, x: True):
        Hierarchy.check(hierarchy_spec)
        self.hierarchy_spec = hierarchy_spec
        self.state = state
        self.filter_f = filter_f
        self.__init_state = copy(self.state)


    def read(self, data_file, mode='r', apply_post_map=False, carry_state=False):
        """

        :param data_file (DataFile):
        :param mode (str):
        :param apply_post_map (bool):
        :param carry_state (bool):
        :return (dict, State):
        """

        if not isinstance(data_file, DataFile):
            raise ValueError("Data file is not a DataFile object.")

        lineno = 0
        value_hierarchy = {}
        value_hierarchy_list = []

        if type(self.hierarchy_spec) is list:
            multi_hierarchy = True
        else:
            multi_hierarchy = False

        if not isinstance(self.state, State):
            raise ValueError("State is a State object")

        if not carry_state:
            current_state = copy(self.state)
        else:
            current_state = self.state

        with open(data_file.file_name, mode) as file:

             for line in file:
                try:
                    data_file.line.store(line[:-1])

                    if data_file.header_lineno == lineno:
                        data_file.line.set_header()
                        lineno += 1
                        continue

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
                            Hierarchy.traverse(hierarchy_spec, data_file, current_state, value_hierarchy_copy)
                            value_hierarchy_list[i] = value_hierarchy_copy

                    else:
                        Hierarchy.traverse(self.hierarchy_spec, data_file.line, current_state, value_hierarchy)

                except (KeyError, ValueError):
                    print("Error occurred when reading line" + str(lineno) + " of " + data_file.file_name)
                    raise

                lineno += 1

        if multi_hierarchy:

            if apply_post_map:
                for hierarchy_spec, value_hierarchy in zip(self.hierarchy_spec, value_hierarchy_list):
                    Hierarchy.apply_post_map(hierarchy_spec, current_state, value_hierarchy)

            return value_hierarchy_list, current_state
        else:
            if apply_post_map:
                Hierarchy.apply_post_map(self.hierarchy_spec, current_state, value_hierarchy)

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
                        Hierarchy.merge(self.hierarchy_spec[i], final_value_hierarchy, value_hierarchy, True, final_state)

            return final_value_hierarchy_list

        else:
            final_value_hierarchy = {}

            for data_file in data_files:
                value_hierarchy, final_state = self.read(data_file, mode, carry_state)
                final_value_hierarchy = \
                    Hierarchy.merge(self.hierarchy_spec, final_value_hierarchy, value_hierarchy, True, final_state)

            return final_value_hierarchy

    def clear_state(self):
        self.state = copy(self.__init_state)

