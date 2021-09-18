from z3 import Length, FreshInt, ForAll, Implies, And, Exists


def get_constants():
    return []


# def int_seq_select(l: list, index: int, to_z3=False) -> int:
#     if to_z3:
#         return l[index]
#     if index is None or index < 0 or index >= len(l):
#         return None
#     return l[index]


def int_seq_len(l: list, to_z3=False) -> int:
    if to_z3:
        return Length(l)
    return len(l)


def all_eq_const(l: list, value: int, top: int, to_z3=False) -> bool:
    if to_z3:
        k = FreshInt('k')
        return ForAll(k, Implies(And(k >= 0, k < top, k < Length(l)), l[k] == value))
    return all(l[k] == value for k in range(min(top, len(l))))


def all_gt_const(l: list, value: int, top: int, to_z3=False) -> bool:
    if to_z3:
        k = FreshInt('k')
        return ForAll(k, Implies(And(k >= 0, k < top, k < Length(l)), l[k] > value))
    return all(l[k] > value for k in range(min(top, len(l))))


def value_in_list(l: list, value: int, to_z3=False) -> bool:
    if to_z3:
        k = FreshInt('k')
        return Exists(k, l[k] == value)
    return value in l

#
# def int_seq_eq(l1: list, l2: list, to_z3=False) -> bool:
#     return l1 == l2


# def int_seq_all_is_const(l: list, const: int, stop_index: int, to_z3=False) -> bool:
#     if to_z3:
#         i = FreshInt('i')
#         return ForAll(i, Or(i < 0, i >= stop_index, l[i] == const))
#     return all(l[i] == const for i in range(stop_index))

#
# def int_seq_prefix_eq(l1: list, l2: list, stop_index: int, to_z3=False) -> bool:
#     if to_z3:
#         i = FreshInt('i')
#         return ForAll(i, Or(i < 0, i >= stop_index, l1[i] == l2[i]))
#     return all(l1[i] == l2[i] for i in range(stop_index))

#
# def int_seq_all_gt(l: list, num: int, stop_index: int, to_z3=False) -> bool:
#     if to_z3:
#         i = FreshInt('i')
#         return ForAll(i, Or(i < 0, i >= stop_index, l[i] > num))
#     return all(l[i] > num for i in range(stop_index))
#
#
# def int_seq_all_lt(l: list, num: int, stop_index: int, to_z3=False) -> bool:
#     if to_z3:
#         i = FreshInt('i')
#         return ForAll(i, Or(i < 0, i >= stop_index, l[i] <= num))
#     return all(l[i] < num for i in range(stop_index))
