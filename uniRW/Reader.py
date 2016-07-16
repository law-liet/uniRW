from .Key import Key, StateKey
from .Value import Value, StateValue
from .File import DataFile


class Reader:

    def __init__(self, Key, Values, State=None, filter_f=lambda dummy,x:True):
        self.Key = Key
        self.Values = Values
        self.State = State
        self.filter_f = filter_f

    def read(self, data_file, mode='r', apply_post_map=False):

        lineno = 0
        key_val_dict = {}
        current_state = None
        if self.State != None:
            current_state = self.State.copy()

        if not isinstance(data_file, DataFile):
            raise ValueError("Data file is not a DataFile object.")

        with open(data_file.file_name, mode) as file:

            for line in file:

                data_file.line.set(line[:-1])

                if data_file.header_lineno == lineno:
                    data_file.line.set_header()
                    lineno += 1
                    continue

                if self.State != None:
                    current_state.update(data_file.line)

                if self.filter_f(current_state, data_file.line):
                    lineno += 1
                    continue

                if isinstance(self.Key, Key):
                    key = self.Key.map_f(current_state, data_file.line.get_by_name(self.Key.name))
                elif isinstance(self.Key, StateKey):
                    key = self.Key.map_f(current_state, current_state.get(self.Key.name))
                else:
                    raise ValueError("Key is not a Key or StateKey object")

                for value in self.Values:

                    val_name = value.name

                    if isinstance(value, StateValue):
                      if value.name in current_state:
                          val = value.map_f(current_state, current_state.get(value.name))
                      else:
                        raise KeyError(str(value.name) + " is not in state")
                    elif isinstance(value, Value):
                        val = value.map_f(current_state, data_file.line.get_by_name(value.name))
                    else:
                        raise ValueError("Value is not a Value or StateValue object")

                    if key in key_val_dict:
                        if val_name in key_val_dict[key]:
                            current_val = key_val_dict[key][val_name]
                            reduced_val = value.reduce_f(current_val, val)
                            key_val_dict[key][val_name] = reduced_val

                        else:
                            key_val_dict[key][val_name] = val
                    else:
                        key_val_dict[key] = {}
                        key_val_dict[key][val_name] = val

                lineno += 1

        def post_map(state, v_dict):
            new_v_dict = v_dict
            for value in self.Values:
                current_val = v_dict[value.name]
                new_v_dict[value.name] = value.post_map_f(state, current_val)
            return new_v_dict

        if apply_post_map:
            final_key_val_dict = {k: post_map(current_state,v_dict) for k, v_dict in key_val_dict.items()}
            return final_key_val_dict, current_state
        else:
            return key_val_dict, current_state


    def readAll(self, data_files, mode='r'):
        pass
