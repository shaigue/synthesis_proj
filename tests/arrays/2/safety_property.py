from z3 import Array, IntSort, Int, Function, And, ForAll, Implies, Sum, If
from config import ARRAY_LEN


def get_safety_property():
    i = Int('i')
    m = Int('m')
    a = Array('a', IntSort(), IntSort())

    return Sum([If(k < i, a[k], 0) for k in range(ARRAY_LEN)]) <= m * i
