# utility functions


def check_and_apply_f(f_dict, f, key, arg):
    return f_dict[key](arg) if key in f_dict else f(arg)


def check_and_apply_2(f_dict, key, arg1, arg2):
    return f_dict[key](arg1,arg2) if key in f_dict else arg2


def idenL(x,dummy):
    return x


def idenR(dummy,x):
    return x


def pureR(f):
    return lambda _,x: f(x)


def pureL(f):
    return lambda x,_: f(x)
