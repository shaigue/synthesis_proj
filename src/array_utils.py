from z3 import Array, IntSort


def get_z3_int_array(name: str):
    return Array(name, IntSort(), IntSort())

