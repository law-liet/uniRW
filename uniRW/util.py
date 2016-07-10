# utility functions

def check_and_apply_f(f_dict, f, key, arg):
  return f_dict[key](arg) if key in f_dict else f(arg)

def check_and_apply_2(f_dict, key, arg1, arg2):
  return f_dict[key](arg1,arg2) if key in f_dict else arg2

def idenL(x,dummy):
  return x

def idenR(dummy,x):
  return x

def to_int(dummy,x):
  return int(x)

def to_float(dummy,x):
  return float(x)

def to_str(dummy,x):
  return str(x)
