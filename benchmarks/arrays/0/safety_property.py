from z3 import Array, IntSort
from config import ARRAY_LEN


# TODO : if we use arrays of unknown sizes, we cannot take the product of all the array elements
def get_safety_property():
    a = Array('a', IntSort(), IntSort())
    prod = a[0]
    for i in range(1, ARRAY_LEN):
        prod = prod * a[i]

    return prod > 0
