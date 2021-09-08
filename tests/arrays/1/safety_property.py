from z3 import Array, IntSort, Int, Function, And, ForAll, Implies, Sum, If
from config import ARRAY_LEN


def get_safety_property():
    i = Int('i')
    a1 = Array('a1', IntSort(), IntSort())
    a2 = Array('a2', IntSort(), IntSort())

    # Get a z3 expression that describes an array's sum
    j = Int('j')
    sumArray1 = Function('sumArray', IntSort(), IntSort())
    sumArray2 = Function('sumArray', IntSort(), IntSort())
    sum_pred1 = And(sumArray1(-1) == 0,
                    ForAll(j, Implies(And(j >= 0, j < ARRAY_LEN), sumArray1(j) == sumArray1(j-1) + a1[j])))
    sum_pred2 = And(sumArray2(-1) == 0,
                    ForAll(j, Implies(And(j >= 0, j < ARRAY_LEN), sumArray2(j) == sumArray2(j-1) + a2[j])))

    return And(sum_pred1, sum_pred2, sumArray1(i-1) == sumArray2(i-1))

def get_safety_property2():
    i = Int('i')
    a1 = Array('a1', IntSort(), IntSort())
    a2 = Array('a2', IntSort(), IntSort())
