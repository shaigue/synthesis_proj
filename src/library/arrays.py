from z3 import Int, ForAll, Or, If, And, FreshInt

from config import ARRAY_LEN


def get_constants():
    # We don't want to support array constants I think.
    return [ARRAY_LEN]


def arr_eq(l1: list, l2: list, to_z3=False) -> bool:
    return l1 == l2


def arr_select(l: list, index: int, to_z3=False) -> int:
    # Works for z3 arrays as well
    try:
        return l[index]
    except IndexError:
        return None


def forall_eq(l: list, num: int, array_end: int, to_z3=False) -> bool:
    if to_z3:
        k = FreshInt()
        return ForAll(k, Or(l[k] == num, k < 0, array_end <= k))
    if array_end >= 0:
        return all(x == num for x in l[:array_end])
    else:
        # Every K is less than 0 or greater than a negative number
        return True


def forall_eq_arrays(l1: list, l2: list, array_end: int, to_z3=False) -> bool:
    if to_z3:
        k = FreshInt()
        return ForAll(k, Or(l1[k] == l2[k], k < 0, array_end <= k))
    if array_end >= 0:
        return l1[:array_end] == l2[:array_end]
    else:
        # Every K is less than 0 or greater than a negative number
        return True


def forall_gt(l: list, num: int, to_z3=False) -> bool:
    # TODO: Not in use for now, if needed, add array_end parameter
    if to_z3:
        k = FreshInt()
        return ForAll(k, Or(l[k] > num, k < 0, ARRAY_LEN <= k))
    return all(x > num for x in l)


def forall_lt(l: list, num: int, array_end: int = ARRAY_LEN, to_z3=False) -> bool:
    if to_z3:
        k = FreshInt()
        return ForAll(k, Or(l[k] <= num, k < 0, array_end <= k))
    if array_end >= 0:
        return all(x <= num for x in l[:array_end])
    else:
        # Every K is less than 0 or greater than a negative number
        return True


def _store(l: list, num: int, index: int):
    new = l.copy()
    new[index] = num
    return new
