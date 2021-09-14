from z3 import Int, ForAll, Or, If, And, FreshInt


def get_constants():
    return []


def arr_eq(l1: list, l2: list, to_z3=False) -> bool:
    return l1 == l2


def arr_select(l: list, index: int, to_z3=False) -> int:
    # TODO: make sure to deal with index errors
    return l[index]


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
        return ForAll(k, Or(l[k] > num, k < 0))
    return all(x > num for x in l)


def forall_lt(l: list, num: int, array_end: int, to_z3=False) -> bool:
    if to_z3:
        k = FreshInt()
        return ForAll(k, Or(l[k] <= num, k < 0, array_end <= k))
    if array_end >= 0:
        return all(x <= num for x in l[:array_end])
    else:
        # Every K is less than 0 or greater than a negative number
        return True
