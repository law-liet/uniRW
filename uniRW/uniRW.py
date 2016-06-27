# My Universal Reader and Writer
# Author: Langxuan Su

from __future__ import print_function

def read(file_name, mode, key_col, val_cols, split_char, header=False,
         header_dict={}, ignore_chars=[], map_fs={}, reduce_fs={}):

  lineno = 0
  headers = header_dict
  key_val_dict = {}

  with open(file_name, mode) as file:

    for line in file:
      if line[0] in ignore_chars: continue
      a = line[:-1].split(split_char)
      key = map_fs['key'](a[key_col]) if 'key' in map_fs else a[key_col]

      if header: 
        if lineno == 0 and headers == {}:
          headers[key_col] = a[key_col]
          for val_col in val_cols: 
            headers[val_col] = a[val_col]
          continue

      for val_col in val_cols:

        val_name = headers[val_col] if header else val_col
        if val_col == 'lineno':
          val = map_fs[val_col](lineno) if val_col in map_fs else lineno
        else:
          val = map_fs[val_col]((a[val_col])) if val_col in map_fs else a[val_col]

        if key in key_val_dict:
          if val_name in key_val_dict[key]:
            current_val = key_val_dict[key][val_name]
            reduced_val = reduce_fs[val_col]((current_val, val)) if val_col in reduce_fs else val
            key_val_dict[key][val_name] = reduced_val

          else:
            key_val_dict[key][val_name] = val
        else:
          key_val_dict[key] = {}
          key_val_dict[key][val_name] = val

      lineno += 1

  key_val_dict['lineno'] = lineno
  return key_val_dict


def readAll(file_names, mode, key_col, val_cols, split_char, header=False,
            header_dict={}, ignore_chars=[], map_fs={}, reduce_fs={},
            post_map_fs={}, post_reduce_fs={}):

  final_key_val_dict = {}
#  lineno = 0

  for file_name in file_names:

    key_val_dict = read(file_name=file_name,
                        mode=mode,
                        key_col=key_col,
                        val_cols=val_cols,
                        split_char=split_char,
                        header=header,
                        header_dict=header_dict,
                        ignore_chars=ignore_chars,
                        map_fs=map_fs,
                        reduce_fs=reduce_fs)

    nline = key_val_dict['lineno']

    for key, val_dict in key_val_dict.items():

      if key == 'lineno': continue

      # deal with lineno in the future

      if key in final_key_val_dict:
        for val_name, raw_val in val_dict.items():
          val = post_map_fs[val_name](raw_val, nline) if val_name in post_map_fs else raw_val
          if val_name in final_key_val_dict[key]:
            current_val = val_dict[val_name]
            reduced_val = \
              post_reduce_fs[val_name](current_val, val) if val_name in post_reduce_fs else val
            final_key_val_dict[key][val_name] = reduced_val
          else:
            final_key_val_dict[key][val_name] = val

      else:
        final_key_val_dict[key] = {}
        for val_name, raw_val in val_dict.items():
          val = post_map_fs[val_name](raw_val, nline) if val_name in post_map_fs else raw_val
          final_key_val_dict[key][val_name] = val

#    lineno += nline

  return final_key_val_dict

def write(file_name, mode, key_val_dict, col_names,
          header, split_char, foreword='', end_char='\n'):

  output = open(file_name, mode)
  header_line = split_char.join(header)
  if foreword != '': print(foreword, file=output)
  print(header_line, file=output)

  for key, val_dict in key_val_dict.items():

    line = ''

    for col_name in col_names:
      if col_name=='key':
        line += str(key)
      else:
        line += str(val_dict[col_name])
      line += split_char

    print(line[:-1], file=output, end=end_char)

  output.close()
