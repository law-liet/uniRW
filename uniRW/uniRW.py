# A Universal Reader and Writer
# Author: Langxuan Su

from __future__ import print_function
import re
from .util import check_and_apply_2
import sys

def read(file_name, mode, key_col, val_cols, split_re, header=False,
         header_dict={}, ignore_chars=[], map_fs={}, reduce_fs={},
         states = {}, update_state = None):

  lineno = 0
  headers = header_dict
  key_val_dict = {}
  current_states = states.copy()

  with open(file_name, mode) as file:

    for line in file:
      if line[0] in ignore_chars: continue
      a = re.split(split_re, line[:-1])
      key = check_and_apply_2(map_fs, 'key', current_states, a[key_col])

      if header:
        if lineno == 0 and headers == {}:
          headers[key_col] = a[key_col]
          for val_col in val_cols:
            headers[val_col] = a[val_col]
          continue

      current_states = update_state(current_states, a) if update_state != None else current_states

      for val_col in val_cols:

        val_name = headers[val_col] if header else val_col
        if type(val_col) is str:
          if val_col in current_states:
            val = check_and_apply_2(map_fs, val_col, current_states, current_states[val_col])
          else:
            print('Error: ' + val_col+' not '+'in states', file=sys.stderr)
            sys.exit()
        else:
          val = check_and_apply_2(map_fs, val_col, current_states, a[val_col])

        if key in key_val_dict:
          if val_name in key_val_dict[key]:
            current_val = key_val_dict[key][val_name]
            reduced_val = check_and_apply_2(reduce_fs, val_col, current_val, val)
            key_val_dict[key][val_name] = reduced_val

          else:
            key_val_dict[key][val_name] = val
        else:
          key_val_dict[key] = {}
          key_val_dict[key][val_name] = val

      lineno += 1

  return (key_val_dict, current_states)


def readAll(file_names, mode, key_col, val_cols, split_re, header=False,
            header_dict={}, ignore_chars=[], map_fs={}, reduce_fs={},
            states = {}, update_state = None, post_map_fs={}, post_reduce_fs={}):

  final_key_val_dict = {}

  for file_name in file_names:

    key_val_dict, final_states = read(file_name=file_name,
                                mode=mode,
                                key_col=key_col,
                                val_cols=val_cols,
                                split_re=split_re,
                                header=header,
                                header_dict=header_dict,
                                ignore_chars=ignore_chars,
                                map_fs=map_fs,
                                reduce_fs=reduce_fs,
                                states = states,
                                update_state = update_state)

    for key, val_dict in key_val_dict.items():

      if key in final_key_val_dict:

        for val_name, raw_val in val_dict.items():

          val = check_and_apply_2(post_map_fs, val_name, final_states, raw_val)

          if val_name in final_key_val_dict[key]:

            current_val = final_key_val_dict[key][val_name]

            reduced_val = check_and_apply_2(post_reduce_fs, val_name, current_val, val)
            final_key_val_dict[key][val_name] = reduced_val
          else:
            final_key_val_dict[key][val_name] = val

      else:
        final_key_val_dict[key] = {}

        for val_name, raw_val in val_dict.items():
          val = check_and_apply_2(post_map_fs, val_name, final_states, raw_val)

          final_key_val_dict[key][val_name] = val

  return final_key_val_dict

def write(file_name, mode, key_val_dict, col_names,
          header, split_char, sort_by=None, foreword='', end_char='\n', epilogue=''):

  output = open(file_name, mode)
  header_line = split_char.join(header)
  if foreword != '': print(foreword, file=output)
  print(header_line, file=output)

  if sort_by==None:
    sorted_items = sorted(key_val_dict.items())
  else:
    sorted_items = sorted(key_val_dict.items(), key = lambda (k,v): v[sort_by])

  for key, val_dict in sorted_items:

    line = ''

    for col_name in col_names:
      if col_name=='key':
        line += str(key)
      else:
        line += str(val_dict[col_name])
      line += split_char

    print(line[:-1], file=output, end=end_char)

  if foreword != '': print(epilogue, file=output)
  output.close()
