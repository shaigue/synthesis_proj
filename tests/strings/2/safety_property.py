from z3 import Strings, PrefixOf, Or


def get_safety_property():
    s, s1, s2 = Strings('s s1 s2')
    return Or(PrefixOf(s2, s), PrefixOf(s1, s))
