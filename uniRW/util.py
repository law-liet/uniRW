# utility functions


def idenL(x, _):
    return x


def idenR(_, x):
    return x


def pureR(f):
    return lambda _, x: f(x)


def pureL(f):
    return lambda x, _: f(x)
