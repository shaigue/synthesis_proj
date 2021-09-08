from z3 import Array, IntSort, Int, Function, And, ForAll, Implies, Sum, If
from config import ARRAY_LEN


def get_safety_property():
    i = Int('i')
    a1 = Array('a1', IntSort(), IntSort())
    a2 = Array('a2', IntSort(), IntSort())

    sum1 = Sum([If(k < i, a1[k], 0) for k in range(ARRAY_LEN)])
    sum2 = Sum([If(k < i, a2[k], 0) for k in range(ARRAY_LEN)])

    return sum1 == sum2
