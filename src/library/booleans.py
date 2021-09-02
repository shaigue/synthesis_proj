"""Boolean functions for the synthesizer"""


def and_(x: bool, y: bool, to_z3=False) -> bool:
    return x and y


def or_(x: bool, y: bool, to_z3=False) -> bool:
    return x or y


def not_(x: bool, to_z3=False) -> bool:
    return not x
