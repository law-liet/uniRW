from __future__ import absolute_import, print_function

from uniRW.util import idenL


class State:

    def __init__(self, init_state, update_func=idenL):
        """Initialize a state for stateful file reading.

        :param init_state (dict): a dictionary (name => value) storing the initial state.
        :param update_func (State * Line -> ()): a function that update state after reading each line.
        """
        self.__state = init_state
        self.update_func = update_func
        self.__read_only = True

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        return self.set(name, value)

    def __contains__(self, name):
        return name in self.__state

    def get(self, name):
        if name not in self.__state:
            raise KeyError(str(name) + " is not in state")
        else:
            return self.__state[name]

    def set(self, name, val):
        if not self.__read_only:
            if name not in self.__state:
                raise KeyError(str(name) + " is not in state")
            else:
                self.__state[name] = val
        else:
            raise KeyError("Error: cannot change state")

    def lock(self):
        self.__read_only = True

    def release(self):
        self.__read_only = False

    def update(self, val):
        if not self.__read_only:
            self.update_func(self, val)
        else:
            raise KeyError("Error: cannot change state")

    def print(self):
        print(self.__state)
