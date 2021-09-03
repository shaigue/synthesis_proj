from z3 import String, Int, Length


def get_safety_property():
    s = String('s')
    x = Int('x')
    return Length(s) <= x
