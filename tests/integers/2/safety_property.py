from z3 import Int


def get_safety_property():
    z = Int('z')
    y = Int('y')
    return z < y
