from __future__ import print_function
from __future__ import absolute_import
from uniRW.util import idenL

class State:

    def __init__(self, init_state, update_func=idenL):
        self.__state = init_state
        self.__update = update_func
        self.__read_only = True

    def check(self, name):
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

    def set_update(self, update_func):
        self.__update = update_func

    def lock(self):
        self.__read_only = True

    def release(self):
        self.__read_only = False

    def update(self, val):
        if not self.__read_only:
            self.__update(self, val)
        else:
            raise KeyError("Error: cannot change state")

    def print(self):
        print(self.__state)
