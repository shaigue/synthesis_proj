# TODO
from typing import List

# TODO: add support for arrays in varying sizes
from z3 import Array, Ints, ForAll, And, Implies, Int, Or

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
    # TODO: leave this inexpressible
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
        is_expressible=True,
    )


def test_2():
    # TODO: pass this also
    def descending_sort(l: List[int]):
        i = j = temp = max_i = 0
        while i < len(l):
            yield locals()
            max_i = i
            for j in range(i, len(l)):
                if l[j] > l[max_i]:
                    max_i = j
            temp = l[i]
            l[i] = l[max_i]
            l[max_i] = temp
            i += 1

    l = IntSeq('l')
    i = Int('i')
    # safety_property = ForAll(k, Or(k < 0, k >= i - 1, l[k] >= l[k + 1]))
    safety_property = Or(i <= 0, l[0] >= l[i-1])
    return Benchmark(
        descending_sort,
        safety_property,
        is_correct=True,
        is_expressible=True
    )


def test_3():
    # TODO: make this pass
    def max_arr(l1: List[int], l2: List[int]):
        l = [0] * len(l1)
        i = 0
        while i < len(l1):
            yield locals()
            l[i] = max(l1[i], l2[i])
            i += 1

    def input_condition(l1: List[int], l2: List[int]):
        return len(l1) == len(l2)

    l = IntSeq('l')
    l1 = IntSeq('l1')
    l2 = IntSeq('l2')
    i = Int('i')
    safety_property = Or(i < 1, And(l[i-1] - l1[i-1] >= 0, l[i-1] - l2[i-1] >= 0))
    return Benchmark(
        max_arr,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )


# TODO: make it so there is 6 tests (test_0 -> test_5)