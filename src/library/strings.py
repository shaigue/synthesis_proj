"""Functions for the string predicate language"""
from z3 import SubString, Concat, Replace, PrefixOf, SuffixOf, Contains, IndexOf, Length


def get_constants():
    return []


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


#
# def str_eq(s1: str, s2: str, to_z3=False) -> bool:
#     return s1 == s2


# def str_contains(s: str, substr: str, to_z3=False) -> bool:
#     if to_z3:
#         return Contains(s, substr)
#     return substr in s
#
#
# def str_concat(s1: str, s2: str, to_z3=False) -> str:
#     if to_z3:
#         return Concat(s1, s2)
#     return s1 + s2
