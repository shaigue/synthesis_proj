# TODO: I would really like to make this part more "functional", i.e. by passing functions instead of explicitly
#   writing a function for every test
# TODO: maybe we should add Existential quantifiers? or putting Not in front of ForAll is enough?
from z3 import Int, ForAll, Or, If, And, FreshInt, Length


def get_constants():
    return []


# def int_seq_len(l: list, to_z3=False) -> int:
#     if to_z3:
#         return Length(l)
#     return len(l)

# TODO: add function to compare 2 array elements 1-1
#
# def int_seq_eq(l1: list, l2: list, to_z3=False) -> bool:
#     return l1 == l2


def int_seq_select(l: list, index: int, to_z3=False) -> int:
    return l[index]


def int_seq_all_is_const(l: list, const: int, stop_index: int, to_z3=False) -> bool:
    if to_z3:
        i = FreshInt('i')
        return ForAll(i, Or(i < 0, i >= stop_index, l[i] == const))
    return all(l[i] == const for i in range(stop_index))

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
