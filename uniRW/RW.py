# A Universal Reader and Writer
# Author: Langxuan Su

from __future__ import print_function
from re import split as resplit
from .util import check_and_apply_f, check_and_apply_2
import sys

def read(file_name, mode, key_col, val_cols, split_re, has_header=False,
         header_dict={}, ignore_chars=[], map_fs={}, reduce_fs={},
         filter_f=None, state={}, update_state=None):

  lineno = 0
  headers = header_dict
  key_val_dict = {}
  current_state = state.copy()

  with open(file_name, mode) as file:

    for line in file:
      if line[0] in ignore_chars: continue
      a = resplit(split_re, line[:-1])

      key = check_and_apply_2(map_fs, 'key', current_state, a[key_col])

      if has_header:
        if lineno == 0:
          if headers == {}:
            headers[key_col] = a[key_col]
            for val_col in val_cols:
              headers[val_col] = a[val_col]
          lineno += 1
          continue

      if update_state != None: update_state(current_state, a)

      if filter_f != None and not filter_f(current_state, a):
        lineno += 1
        continue

      for val_col in val_cols:

        val_name = headers[val_col] if val_col in headers else val_col
        if type(val_col) is str:
          if val_col in current_state:
            val = check_and_apply_2(map_fs, val_col, current_state, current_state[val_col])
          else:
            print('Error:' + val_col + ' not ' + 'in states', file=sys.stderr)
            sys.exit()
        else:
          val = check_and_apply_2(map_fs, val_col, current_state, a[val_col])

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

  return (key_val_dict, current_state)


def readAll(file_names, mode, key_col, val_cols, split_re, has_header=False,
            header_dict={}, ignore_chars=[], map_fs={}, reduce_fs={}, filter_f=None,
            state={}, update_state=None, post_map_fs={}, post_reduce_fs={}):

  final_key_val_dict = {}

  for file_name in file_names:

    key_val_dict, final_state = read(file_name= file_name,
                                     mode= mode,
                                     key_col= key_col,
                                     val_cols= val_cols,
                                     split_re= split_re,
                                     has_header= has_header,
                                     header_dict= header_dict,
                                     ignore_chars= ignore_chars,
                                     map_fs= map_fs,
                                     reduce_fs= reduce_fs,
                                     filter_f= filter_f,
                                     state= state,
                                     update_state= update_state)

    for key, val_dict in key_val_dict.items():

      if key in final_key_val_dict:

        for val_name, raw_val in val_dict.items():

          val = check_and_apply_2(post_map_fs, val_name, final_state, raw_val)

          if val_name in final_key_val_dict[key]:

            current_val = final_key_val_dict[key][val_name]

            reduced_val = check_and_apply_2(post_reduce_fs, val_name, current_val, val)
            final_key_val_dict[key][val_name] = reduced_val
          else:
            final_key_val_dict[key][val_name] = val

      else:
        final_key_val_dict[key] = {}

        for val_name, raw_val in val_dict.items():
          val = check_and_apply_2(post_map_fs, val_name, final_state, raw_val)

          final_key_val_dict[key][val_name] = val

  return final_key_val_dict

def write(file_name, mode, key_val_dict, col_names, header, split_char,
          to_string={}, sort_by=None, foreword=[], end_char='\n', epilogue=[]):

  output = open(file_name, mode)
  header_line = split_char.join(header)
  for foreword_line in foreword:
    print(foreword_line, file=output)
  print(header_line, file=output)

  if sort_by==None:
    sorted_items = sorted(key_val_dict.items())
  else:
    sorted_items = sorted(key_val_dict.items(), key= lambda (k,v): v[sort_by])

  for key, val_dict in sorted_items:

    line = ''

    for col_name in col_names:
      if col_name=='key':
        line += check_and_apply_f(to_string, str, col_name, key)
      else:
        line += check_and_apply_f(to_string, str, col_name, val_dict[col_name])
      line += split_char

    print(line[:-1], file=output, end=end_char)

  for epilogue_line in epilogue:
    print(epilogue_line, file=output)
  output.close()
