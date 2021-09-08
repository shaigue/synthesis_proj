from z3 import Array, IntSort, Int, Function, And, ForAll, Implies
from config import ARRAY_LEN


def get_safety_property():
    i = Int('i')
    m = Int('m')
    a = Array('a', IntSort(), IntSort())

    # Get a z3 expression that describes an array's sum
    j = Int('j')
    sumArray = Function('sumArray', IntSort(), IntSort())
    sum_pred = And(sumArray(-1) == 0,
                   ForAll(j, Implies(And(j >= 0, j < ARRAY_LEN), sumArray(j) == sumArray(j-1) + a[j])))

    return And(sum_pred, sumArray(i-1) <= m * i)