from z3 import String, And, PrefixOf, SuffixOf


def get_safety_property():
    s1 = String('s1')
    s = String('s')
    s2 = String('s2')
    return And(PrefixOf(s1, s), SuffixOf(s2, s))
