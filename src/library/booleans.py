"""Boolean functions for the synthesizer"""
from z3 import And, Or, Not


def and_(x: bool, y: bool, to_z3=False) -> bool:
    if to_z3:
        return And(x, y)
    return x and y


def or_(x: bool, y: bool, to_z3=False) -> bool:
    if to_z3:
        return Or(x, y)
    return x or y


def not_(x: bool, to_z3=False) -> bool:
    if to_z3:
        return Not(x)
    return not x
