from z3 import String, IndexOf
# TODO: note that the grammar cannot produce this rule!


def get_safety_property():
    s = String('s')
    return IndexOf(s, 'x') == 0
