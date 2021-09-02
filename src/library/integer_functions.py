"""Functions to use for integer programs
make sure that every entry has a type annotation, and return type annotation
and the last argument is to_z3, with false default value that deals with inputs from z3.
"""


def add(x: int, y: int, to_z3=False) -> int:
    return x + y


def sub(x: int, y: int, to_z3=False) -> int:
    return x - y


def mul(x: int, y: int, to_z3=False) -> int:
    return x * y


def eq(x: int, y: int, to_z3=False) -> bool:
    return x == y


def lt(x: int, y: int, to_z3=False) -> bool:
    return x < y
