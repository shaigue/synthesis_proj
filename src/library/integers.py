"""
Functions to use for integer programs
make sure that every entry has a type annotation, and return type annotation
and the last argument is to_z3, with false default value that deals with inputs from z3.
"""


def get_constants():
    return [0, 1]


def int_add(x: int, y: int, to_z3=False) -> int:
    return x + y


def int_sub(x: int, y: int, to_z3=False) -> int:
    return x - y


# def mul(x: int, y: int, to_z3=False) -> int:
#     return x * y


def int_eq(x: int, y: int, to_z3=False) -> bool:
    return x == y


def int_lt(x: int, y: int, to_z3=False) -> bool:
    return x < y
