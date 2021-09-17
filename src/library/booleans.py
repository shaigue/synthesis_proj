"""Boolean functions for the synthesizer"""
from z3 import And, Or, Not


def or_(x: bool, y: bool, to_z3=False) -> bool:
    if to_z3:
        return Or(x, y)

    if x is None:
        if y is None or not y:
            return None
        return True

    if y is None:
        if x is None or not x:
            return None
        return True

    return x or y


def not_(x: bool, to_z3=False) -> bool:
    if to_z3:
        return Not(x)
    if x is None:
        return None

    return not x

#
# def and_(x: bool, y: bool, to_z3=False) -> bool:
#     if to_z3:
#         return And(x, y)
#     return x and y

