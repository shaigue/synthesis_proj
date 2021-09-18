from typing import List

from z3 import Ints, ForAll, Implies, Int, Or, Length, And, Exists

from src.utils.int_seq_utils import IntSeq
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

    safety_property = ForAll(k, Implies(And(k >= 0, k < i), l[k] == x))

    return Benchmark(
        set_const,
        safety_property,
        is_correct=True,
        is_expressible=True
    )


def test_1():
    def greater_arr(x: int, y: int, size: int):
        if x == y:
            y += 1
        l1 = []
        l2 = []
        i = 0
        while i < size:
            yield locals()
            l1.append(x)
            l2.append(y)
            i += 1

    def input_condition(x: int, y: int, size: int) -> bool:
        return size > 0

    l1 = IntSeq('l1')
    l2 = IntSeq('l2')
    k = Int('k')

    safety_property = Or(ForAll(k, Implies(And(k >= 0, k < Length(l1)), l1[k] > l2[k])),
                         ForAll(k, Implies(And(k >= 0, k < Length(l1)), l1[k] < l2[k])))

    return Benchmark(
        greater_arr,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )


def test_2():
    def almost_const_arr(x: int, size: int):
        l = []
        i = 0
        while i < size:
            yield locals()
            l.append(x + (i % 2))
            i += 1

    def input_condition(x: int, size: int):
        return size > 0

    l = IntSeq('l')
    x, k = Ints('x k')

    safety_property = ForAll(k, Implies(And(k >= 0, k < Length(l)), l[k] >= x))
    return Benchmark(
        almost_const_arr,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )


def test_3():
    def shared_min(l1: List[int], l2: List[int]):
        m = min(l1[0], l2[0])
        i1 = i2 = 0
        while i1 + i2 < len(l1) + len(l2):
            yield locals()
            if i1 < len(l1):
                m = min(m, l1[i1])
                i1 += 1
            else:
                m = min(m, l2[i2])
                i2 += 1

    def input_condition(l1: List[int], l2: List[int]):
        return len(l1) > 0 and len(l2) > 0

    l1 = IntSeq('l1')
    l2 = IntSeq('l2')
    m, i1, i2, k = Ints('m i1 i2 k')

    safety_property = Exists(k, Or(l1[k] == m, l2[k] == m))

    return Benchmark(
        shared_min,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
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
            yield locals()
            max_i = l[i:].index(max(l[i:]))
            l[i], l[max_i] = l[max_i], l[i]
            i += 1

    def input_condition(l: List[int]):
        return len(l) > 2

    l = IntSeq('l')
    i = Int('i')
    safety_property = Or(i < 1, i >= Length(l), l[i-1] >= l[i])
    return Benchmark(
        descending_sort,
        safety_property,
        is_correct=False,
        is_expressible=False,
        input_condition=input_condition
    )
