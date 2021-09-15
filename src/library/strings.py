"""Functions for the string predicate language"""
from z3 import SubString, Concat, Replace, PrefixOf, SuffixOf, Contains, IndexOf, Length

# TODO: maybe start with a limited set of options, and then increase the number of predicates


def get_constants():
    # TODO: maybe make that strings are over uppercase alphabet?
    return []


def str_eq(s1: str, s2: str, to_z3=False) -> bool:
    return s1 == s2


def str_len(s: str, to_z3=False) -> int:
    if to_z3:
        return Length(s)
    return len(s)


def str_prefix_of(prefix: str, s: str, to_z3=False) -> bool:
    if to_z3:
        return PrefixOf(prefix, s)
    return s.startswith(prefix)


def str_suffix_of(suffix: str, s: str, to_z3=False) -> bool:
    if to_z3:
        return SuffixOf(suffix, s)
    return s.endswith(suffix)


def str_contains(s: str, substr: str, to_z3=False) -> bool:
    if to_z3:
        return Contains(s, substr)
    return substr in s


def str_concat(s1: str, s2: str, to_z3=False) -> str:
    if to_z3:
        return Concat(s1, s2)
    return s1 + s2

# def str_get_substr(s: str, start_index: int, length: int, to_z3=False) -> str:
#     # TODO: this might throw an exception for different values of parameters,
#     #  so make sure to deal with those in the enumeration procedure
#     if to_z3:
#         return SubString(s, start_index, length)
#     return s[start_index:start_index+length]


# def str_index_of(s: str, substr: str, to_z3=False) -> int:
#     # TODO: what to do with return value when it is not a substring? what should we do?
#     if to_z3:
#         return IndexOf(s, substr)
#     return s.find(substr)


# TODO: I think that this function is redundant, since it's functionality is contained in
#  substr function, should be deleted?
# TODO: add string equivalence function
# def str_char_at_index(s: str, index: int, to_z3=False) -> str:
#     if to_z3:
#         return SubString(s, index, 1)
#     return s[index]


# def str_replace(s: str, old: str, new: str, to_z3=False) -> str:
#     # TODO: does it work well also when the old string is not contained s?
#     if to_z3:
#         return Replace(s, old, new)
#     return s.replace(old, new, 1)

