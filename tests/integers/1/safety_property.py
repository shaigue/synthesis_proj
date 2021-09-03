from z3 import Int


def get_safety_property():
    y = Int('y')
    x = Int('x')
    return y < x + 2
