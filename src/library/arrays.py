from z3 import Int, ForAll, Or

from config import ARRAY_LEN


def get_constants():
    # We don't want to support array constants I think.
    return []


def arr_eq(l1: list, l2: list, to_z3=False) -> bool:
    return l1 == l2


def arr_select(l: list, index: int, to_z3=False) -> int:
    # Works for z3 arrays as well
    return l[index]


def forall_eq(l: list, num: int, to_z3=False) -> bool:
    if to_z3:
        i = Int('i')
        return ForAll(i, Or(l[i] == num, i < 0, ARRAY_LEN <= i))
    return all(x == num for x in l)


def forall_gt(l: list, num: int, to_z3=False) -> bool:
    if to_z3:
        i = Int('i')
        return ForAll(i, Or(l[i] > num, i < 0, ARRAY_LEN <= i))
    return all(x > num for x in l)


def forall_lt(l: list, num: int, to_z3=False) -> bool:
    if to_z3:
        i = Int('i')
        return ForAll(i, Or(l[i] < num, i < 0, ARRAY_LEN <= i))
    return all(x < num for x in l)
