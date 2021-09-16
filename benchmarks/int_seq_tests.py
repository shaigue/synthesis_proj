from typing import List

# TODO: add support for arrays in varying sizes
from z3 import Array, Ints, ForAll, And, Implies, Int, Or, Length

from src.int_seq_utils import IntSeq
from src.test_utils.benchmark import Benchmark


def test_0():
    def set_const(l: List[int], x: int):
        i = 0
        while i < len(l):
            yield locals()
            l[i] = x
            i += 1

    l = IntSeq('l')
    x, i, k = Ints('x i k')

    safety_property = ForAll(k, Or(k < 0, k >= i, l[k] == x))
    return Benchmark(
        set_const,
        safety_property,
        is_correct=True,
        is_expressible=True
    )


def test_1():
    def descending_sort(l: List[int]):
        i = max_i = 0
        while i < len(l):
            if i != 0:
                # Range issues...
                yield locals()
            max_i = l[i:].index(max(l[i:]))
            l[i], l[max_i + i] = l[max_i + i], l[i]
            i += 1

    l = IntSeq('l')
    i = Int('i')
    safety_property = Or(i <= 0, i >= Length(l), l[i-1] - l[i] >= 0)
    return Benchmark(
        descending_sort,
        safety_property,
        is_correct=True,
        is_expressible=True
    )


def test_4():
    def multiply_by_2(l: List[int]):
        i = 0
        l0 = [0] * len(l)
        while i < len(l):
            yield locals()
            l0[i] = l[i] + l[i]
            i += 1

    i, k = Ints('i k')
    l = IntSeq('l')
    l0 = IntSeq('l0')
    safety_property = ForAll(k, Or(k < 0, k >= i, l0[k] == 2 * l[k]))
    return Benchmark(
        multiply_by_2,
        safety_property,
        is_correct=True,
        is_expressible=False,
    )


def test_5():
    def descending_sort(l: List[int]):
        i = max_i = 0
        while i < len(l):
            if i != 0:
                # Range issues...
                yield locals()
            max_i = l[i:].index(max(l[i:]))
            l[i], l[max_i] = l[max_i], l[i]
            i += 1

    l = IntSeq('l')
    i = Int('i')
    # safety_property = ForAll(k, Or(k < 0, k >= i - 1, l[k] >= l[k + 1]))
    safety_property = Or(i <= 0, i >= Length(l), l[i-1] >= l[i])
    return Benchmark(
        descending_sort,
        safety_property,
        is_correct=False,
        is_expressible=False
    )


# TODO: make it so there is 6 tests (test_0 -> test_5)