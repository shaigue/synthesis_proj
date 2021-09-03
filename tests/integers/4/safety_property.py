from z3 import Int


def get_safety_property():
    y = Int('y')
    return y >= 0
