from __future__ import absolute_import

from copy import deepcopy

from uniRW.State import State
from uniRW.Value import GeneralValue, Value, StateValue


class Hierarchy:
    """A hierarchy specification of values defines the format of data being read or written.

    Type 1 (list): represents values in the same layer (usually at the bottom)
    Type 2 (dict): represents the value in the current layer and sub-hierarchy of next layer
    Type 3 (tuple): similar to Type 2 (not recommended because of lack of testing)

    A valid hierarchy specification would be a composition of the above three types following these Specs:

    Spec 1 (list): only GeneralValue objects or Type 3 objects.
    Spec 2 (dict): only one key-value pair, i.e. len(list(hierarchy_spec.items())) == 1.
                   for the key-value pair, key must be a GeneralValue object but value can be Type 1,2 or 3 objects.
    Spec 3 (tuple): a 2-tuple, where the left entry can be anything but right entry must be Type 1,2 or 3

    Example of a valid hierarchy specification: (used in later comments)
    {
        name: {
            subject: [
                rank,
                grade
            ]
        }
    }
    (where rank has name 'Rank', and grade has name 'Grade')

    Example of a dictionary with respect to that hierarchy:
    {
        'Alice': {
            'Math': {
                'Rank': 1,
                'Grade': 4.0
            },
            'CS': {
                'Rank': 2,
                'Grade': 3.9
            }
        },
        'Bob': {
            'Math': {
                'Rank': 2,
                'Grade': 3.9
            },
            'CS': {
                'Rank': 1,
                'Grade': 4.0
        }
    }

    Some terms used in comments:
        "Leaf": the values at the bottom, like grade, rank above.
        "Node": the values not at the bottom, like name, subject above.
        "Branch": a root-to-leaves path, like {'Name': 'Alice', 'Subject': 'Math', 'Rank': 1, 'Grade': 4.0}
    """

    @classmethod
    def check(cls, hierarchy_spec):
        """Check whether the input is a valid hierarchy specification.

        :param hierarchy_spec: an input to be checked.
        :raise some error if hierarchy is not invalid.
        """
        check = cls.check
        try:
            if type(hierarchy_spec) is list:  # Type 1
                for value in hierarchy_spec:
                    if not isinstance(value, GeneralValue):
                        # See whether is Type 3 and check next layer
                        _, next_layer = hierarchy_spec
                        check(next_layer)

            elif type(hierarchy_spec) is dict:  # Type 2
                items = list(hierarchy_spec.items())
                if len(items) != 1:
                    raise ValueError
                else:
                    _, next_layer = items[0]
                    check(next_layer)
            else:  # Type 3
                _, next_layer = hierarchy_spec
                check(next_layer)
        except:
            print("Invalid hierarchy specification")
            raise

    @classmethod
    def apply_post_map(cls, hierarchy_spec, value_hierarchy, state=State({})):
        """Apply post_map to every value at the "leaf" of hierarchy.

        :param hierarchy_spec: a valid hierarchy (or sub-hierarchy).
        :param state (State): a state maybe used in post_map.
        :param value_hierarchy (dict): a dictionary to apply post_map with respect to hierarchy_spec.

        Example:
            Suppose post_map for both rank and grade is +1
            (value hierarchy) before:
                {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}}}

            (value hierarchy) after:
                {'Alice': {'Math': {'Rank': 2, 'Grade': 5.0}}}
        """
        def apply_post_map(hierarchy_spec, value_hierarchy, state):
            if type(hierarchy_spec) is list:  # Type 1

                for value in hierarchy_spec:
                    if isinstance(value, GeneralValue):
                        # Type 1: at the "leaf" of hierarchy
                        val_name = value.name
                        val = value.post_map_f(state, value_hierarchy[val_name])
                        value_hierarchy[val_name] = val
                    else:
                        # Type 3: at the "node" of hierarchy, go to next hierarchy_spec
                        val, next_layer = value
                        apply_post_map(next_layer, value_hierarchy[val], state)

            elif type(hierarchy_spec) is dict:  # Type 2: at the "node" of hierarchy, go to next hierarchy_spec
                value, next_layer = list(hierarchy_spec.items())[0]
                for val, _ in value_hierarchy.items():
                    apply_post_map(next_layer, value_hierarchy[val], state)

            else:  # Type 3: at the "node" of hierarchy, go to next hierarchy_spec
                val, next_layer = hierarchy_spec
                apply_post_map(next_layer, value_hierarchy[val], state)

        apply_post_map(hierarchy_spec, value_hierarchy, state)


    @classmethod
    def traverse(cls, hierarchy_spec, line, state, value_hierarchy):
        """Store the values in the line in the input dictionary by traversing the hierarchy.

        :param hierarchy_spec: a valid hierarchy (or sub-hierarchy).
        :param line (Line or dict): the current line read.
        :param current_state (State or dict): the current state maybe used in map.
        :param value_hierarchy (dict): the dictionary to store values.

        Example:
            Read (line):
                "Alice,Math,1,4.0"
            Add to (value_hierarchy) and merge if necessary:
                {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}}}

        """
        merge = cls.merge
        def traverse(hierarchy_spec, line, state, value_hierarchy):
            if type(hierarchy_spec) is list:  # Type 1

                for value in hierarchy_spec:

                    if isinstance(value, StateValue):
                        # get value from state and apply map
                        val_name = value.name
                        val = value.map_f(state, state[val_name])
                    elif isinstance(value, Value):
                        # get value from line and apply map
                        val_name = value.name
                        val = value.map_f(state, line[val_name])
                    else:
                        # Type 3: store value and go to next layer
                        val, next_layer = value
                        value_hierarchy[val] = {}
                        traverse(next_layer, line, state, value_hierarchy[val])

                    # if another value is already stored, apply reduce and store the value in dictionary
                    if val_name in value_hierarchy:
                        current_val = value_hierarchy[val_name]
                        reduced_val = value.reduce_f(current_val, val)
                        value_hierarchy[val_name] = reduced_val
                    else:
                        value_hierarchy[val_name] = val

            elif type(hierarchy_spec) is dict:  # Type 2

                value, next_layer = list(hierarchy_spec.items())[0]

                if isinstance(value, StateValue):
                    # get value from state and apply map
                    val_name = value.name
                    val = value.map_f(state, state[val_name])
                elif isinstance(value, Value):
                    # get value from line and apply map
                    val_name = value.name
                    val = value.map_f(state, line[val_name])
                else:
                    raise ValueError("Invalid hierarchy specification.")

                if val in value_hierarchy:
                    # if value already stored, go to next layer and merge with current hierarchy
                    new_hierarchy = {}
                    traverse(next_layer, line, state, new_hierarchy)
                    current_hierarchy = value_hierarchy[val]
                    merged_hierarchy = merge(next_layer, current_hierarchy, new_hierarchy)
                    value_hierarchy[val] = merged_hierarchy

                else:
                    # store value and go to next layer
                    value_hierarchy[val] = {}
                    traverse(next_layer, line, state, value_hierarchy[val])

            else:  # Type 3: store value and go to next layer
                val, next_layer = hierarchy_spec
                value_hierarchy[val] = {}
                traverse(next_layer, line, state, value_hierarchy[val])

        traverse(hierarchy_spec, line, state, value_hierarchy)

    @classmethod
    def merge(cls, hierarchy_spec, value_hierarchy1, value_hierarchy2, post=False, state=State({}), top=True):
        """Merge two value hierarchies according to a hierarchy specification.

        :param hierarchy_spec: a valid hierarchy specification.
        :param value_hierarchy1 (dict): a dictionary with respect to hierarchy_spec.
        :param value_hierarchy2 (dict): a dictionary with respect to hierarchy_spec.
        :param post (bool): apply map, reduce or apply post_map, post_reduce
        :param state (State): the current state maybe used in map or post_map
        :param top (bool): whether to copy the input (value_hierarchy1)
        :return (dict): the merged value hierarchy

        Example 1:
            (value_hierarchy1):
                {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}}}
            (value_hierarchy2):
                {'Alice': {'CS': {'Rank': 2, 'Grade': 3.9}}}

            Merge:
                {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}, 'CS': {'Rank': 2, 'Grade': 3.9}}}

        Example 2: (Suppose reduce_f of grade is max, reduce_f of rank is min)
            (value_hierarchy1):
                {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}}}
            (value_hierarchy2):
                {'Alice': {'Math': {'Rank': 2, 'Grade': 3.9}}}

            Merge:
                {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}}

        """
        apply_post_map = cls.apply_post_map

        def merge(hierarchy_spec, value_hierarchy1, value_hierarchy2, post, state, top):

            if top:  # prevent contamination of the top level input dictionary
                merged_hierarchy = deepcopy(value_hierarchy1)
            else:
                merged_hierarchy = value_hierarchy1.copy()
            if top and post:  # apply post map at the top level
                apply_post_map(hierarchy_spec, merged_hierarchy, state)

            if type(hierarchy_spec) is list:  # Type 1

                for value in hierarchy_spec:

                    if isinstance(value, GeneralValue):
                        # apply reduce (or post_map, post_reduce) to "leaf" values
                        val_name = value.name
                        val1 = merged_hierarchy[val_name]
                        val2 = value_hierarchy2[val_name]
                        if post:
                            new_val1 = val1  # already apply post map
                            new_val2 = value.post_map_f(state, val2)
                            new_val = value.post_reduce_f(new_val1, new_val2)
                        else:
                            new_val = value.reduce_f(val1, val2)
                        merged_hierarchy[val_name] = new_val

                    else:  # Type 3: at "node", merge next layer
                        val, next_layer = value
                        merged_hierarchy[val] = \
                            merge(next_layer, merged_hierarchy[val], value_hierarchy2[val], post, state, False)

            elif type(hierarchy_spec) is dict:  # Type 2: at "node", merge every sub-hierarchy
                _, next_layer = list(hierarchy_spec.items())[0]
                for val, next_val_layer2 in value_hierarchy2.items():
                    if val in merged_hierarchy:
                        next_val_layer1 = merged_hierarchy[val]
                        merged_hierarchy[val] = \
                            merge(next_layer, next_val_layer1, next_val_layer2, post, state, False)
                    else:
                        if post:
                            apply_post_map(next_layer, next_val_layer2, state)
                        merged_hierarchy[val] = next_val_layer2

            else:  # Type 3: at "node", merge next layer
                val, next_layer = hierarchy_spec
                merged_hierarchy[val] = \
                    merge(next_layer, merged_hierarchy[val], value_hierarchy2[val], post, state, False)

            return merged_hierarchy

        return merge(hierarchy_spec, value_hierarchy1, value_hierarchy2, post, state, top)

    @classmethod
    def flatten(cls, hierarchy_spec, value_hierarchy):
        """Convert a value hierarchy to all "branches" with respect to a hierarchy specification.

        :param hierarchy_spec: a valid hierarchy specification.
        :param value_hierarchy (dict): a dictionary with respect to hierarchy_spec.

        Example:
            Convert (value_hierarchy):
                {'Alice': {'Math': {'Rank': 1, 'Grade': 4.0}, 'CS': {'Rank': 2, 'Grade': 3.9}}}

            To (value_lines):
                [
                    {'Name': 'Alice', 'Subject': 'Math', 'Rank': 1, 'Grade': 4.0},
                    {'Name': 'Alice', 'Subject': 'CS', 'Rank': 2, 'Grade': 3.9}
                ]
        """
        value_lines = []

        def flatten_helper(hierarchy_spec, value_hierarchy, value_lines, value_line={}):
            if type(hierarchy_spec) is list:  # Type 1
                current_value_line = value_line
                for value in hierarchy_spec:
                    if isinstance(value, GeneralValue):
                        # at "leaf", store (value name => value) in current value line
                        val_name = value.name
                        current_value_line[val_name] = value_hierarchy[val_name]
                    else:  # Type 3: at "node", go to next layer
                        val, next_layer = value
                        flatten_helper(next_layer, value_hierarchy[val], value_lines, current_value_line)
                value_lines.append(current_value_line)  # finish a "branch"

            elif type(hierarchy_spec) is dict:  # Type 2: at "node"
                for root, next in value_hierarchy.items():
                    current_value_line = value_line.copy()  # copy the current value line to different sub-hierarchies
                    value, next_layer = list(hierarchy_spec.items())[0]
                    current_value_line[value.name] = root  # store the current "node"
                    flatten_helper(next_layer, next, value_lines, current_value_line)  # flatten next layer

            else:  # Type 3: at "node", go to next layer
                current_value_line = value_line
                val, next_layer = hierarchy_spec
                flatten_helper(next_layer, value_hierarchy[val], value_lines, current_value_line)

        flatten_helper(hierarchy_spec, value_hierarchy, value_lines)
        return value_lines

    @classmethod
    def traverse_lines(cls, hierarchy_spec, value_lines, state=State({}), filter_f=lambda _, x: True):
        """Covert a list of lines to a dictionary with respect to hierarchy spec (backward of flatten).

        :param hierarchy_spec: a valid hierarchy specification
        :param value_lines ([dict]): a list of (name => value) dictionary
        :param state (State or dict): the evolving state used in map/post_map/filter
        :param filter_f (State * Line -> bool): the predicate for filtering lines with access to state.
        :return: the result dictionary
        """
        value_hierarchy = {}
        traverse = cls.traverse

        release = state.release
        update = state.update
        lock = state.lock

        def update_state(line):
            release()
            update(line)
            lock()

        for line in value_lines:

            # update state
            update_state(line)

            # filter out a line if predicate returns false
            if not filter_f(state, line):
                continue

            # traverse a line with respect to hierarchy
            traverse(hierarchy_spec, line, state, value_hierarchy)

        return value_hierarchy
