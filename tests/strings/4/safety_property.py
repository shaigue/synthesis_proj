from z3 import Strings, Length


def get_safety_property():
    s, s1 = Strings('s s1')
    return Length(s) < Length(s1)
