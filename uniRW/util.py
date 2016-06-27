# utility functions

def check_and_apply1(f_dict, key, arg):
  return f_dict[key](avg) if key in f_dict else arg

def check_and_apply_2(f_dict, key, arg1, arg2):
  return f_dict[key](avg1,arg2) if key in f_dict else arg2