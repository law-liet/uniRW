from __future__ import absolute_import

from copy import deepcopy

from uniRW.File import DataFile
from uniRW.Hierarchy import Hierarchy
from uniRW.State import State


class HReader:

    def __init__(self, hierarchy_spec, state=State({}), filter_f=lambda _, x: True):
        """Initialize the reader.

        :param hierarchy_spec: a (or a list of) hierarchy specification (described in Hierarchy.py).
        :param state (State): the state involved in reading.
        :param filter_f (State * Line -> bool): the predicate for filtering lines with access to state.
        """
        Hierarchy.check(hierarchy_spec)
        if not isinstance(state, State):
            raise ValueError("State is a State object")

        self.hierarchy_spec = hierarchy_spec
        self.state = state
        self.filter_f = filter_f
        self.__init_state = deepcopy(self.state)

    def read_lines(self, value_lines, apply_post_map=False, carry_state=False):
        """Store the data in a list of lines with respect to the hierarchy specification of values

        :param value_lines ([dict]): a list of (name => value) dictionary
        :param apply_post_map (bool): whether apply post_map or not
        :param carry_state: whether mutate the input state
        :return (dict): the result dictionary and the final state.
        """
        # if not carry state, copy the state object such that the input state is not mutated.
        if not carry_state:
            current_state = deepcopy(self.state)
        else:
            current_state = self.state

        value_hierarchy = Hierarchy.traverse_lines(self.hierarchy_spec, value_lines, current_state, self.filter_f)

        # apply post_map_f in each value if apply_post_map is true
        if apply_post_map:
            Hierarchy.apply_post_map(self.hierarchy_spec, value_hierarchy, current_state)

        return value_hierarchy, current_state


    def read(self, data_file, mode='r', apply_post_map=False, carry_state=False):
        """Read a file to store the data with respect to the hierarchy specification of values.

        :param data_file (DataFile): the file to read.
        :param mode (str): reading mode ('r', 'r+', ...).
        :param apply_post_map (bool): whether apply post_map for each value or not.
        :param carry_state (bool): whether keep the mutated state or not.
        :return (dict, State): the result dictionary and the final state.
        """
        if not isinstance(data_file, DataFile):
            raise ValueError("Data file is not a DataFile object.")

        lineno = 0
        value_hierarchy = {}

        # if not carry state, copy the state object such that the input state is not mutated.
        if not carry_state:
            current_state = deepcopy(self.state)
        else:
            current_state = self.state

        filter_f = self.filter_f
        hierarchy_spec = self.hierarchy_spec

        file_name = data_file.file_name
        line = data_file.line
        header_lineno = data_file.header_lineno

        store_line = line.store
        set_line_header = line.set_header

        release = current_state.release
        update = current_state.update
        lock = current_state.lock

        traverse = Hierarchy.traverse

        def update_state(line):
            release()
            update(line)
            lock()

        with open(file_name, mode) as file:

            for data_line in file:
                try:
                    # read a line
                    store_line(data_line[:-1])

                    # set header if header line number matches
                    if header_lineno == lineno:
                        set_line_header()
                        lineno += 1
                        continue

                    # update state
                    # current_state.release()
                    # current_state.update(line)
                    # current_state.lock()
                    update_state(line)

                    # filter out a line if predicate returns false
                    if not filter_f(current_state, line):
                        lineno += 1
                        continue

                    # traverse a line with respect to hierarchy
                    traverse(hierarchy_spec, line, current_state, value_hierarchy)

                except (KeyError, ValueError):
                    print("Error occurred when reading line %s of %s" % (str(lineno+1), file_name))
                    raise

                lineno += 1

        # apply post_map_f in each value if apply_post_map is true
        if apply_post_map:
            Hierarchy.apply_post_map(hierarchy_spec, value_hierarchy, current_state)

        return value_hierarchy, current_state

    def read_all(self, data_files, mode='r', carry_state=False):
        """Read multiple files and store the data with respect to the hierarchy specification of values.

        :param data_files: list of files
        :return: the result dictionary
        """
        final_value_hierarchy = {}

        merge = Hierarchy.merge
        read = self.read
        hierarchy_spec = self.hierarchy_spec
        # read each file and merge the result dictionary
        for data_file in data_files:
            value_hierarchy, final_state = read(data_file, mode, carry_state)
            final_value_hierarchy = \
                merge(hierarchy_spec, final_value_hierarchy, value_hierarchy, True, final_state, False)

        return final_value_hierarchy

    def clear_state(self):
        self.state = deepcopy(self.__init_state)
