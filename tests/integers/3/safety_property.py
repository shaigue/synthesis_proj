from z3 import Ints


def get_safety_property():
    x, y, z = Ints('x y z')
    return z + y <= x
