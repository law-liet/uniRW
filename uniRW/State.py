import sys
from .util import iden

class State:

    def __init__(self, init_states, update_func=iden):
        self.__states = init_states
        self.__update = update_func

    def get(self, name):
        if name not in self.__states:
            print("Error: " + str(name) + " is not in state", file=sys.stderr)
            sys.exit()
        return self.__states[name]

    def set(self, name, val):
        if name not in self.__states:
            print("Error: " + str(name) + " is not in state", file=sys.stderr)
            sys.exit()
        self.__states[name] = val

    def set_update(self, update_func):
        self.__update = update_func

    def update(self):
        self.__states = self.__update(self.__states)

    def print_state(self):
        print(self.__states)
