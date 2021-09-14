# TODO
from typing import List

# TODO: add support for arrays in varying sizes
from z3 import Array, Ints, ForAll, And

from src.array_utils import get_z3_int_array
from src.test_utils.benchmark import Benchmark


def test_0():
    # TODO: pass
    def program(a: List[int], x: int):
        i = 0
        while i < len(a):
            yield locals()
            a[i] = x
            i += 1

    a = get_z3_int_array('a')
    x, i, k = Ints('x i k')

    safety_property = ForAll([k], And(k >= 0, k < i, a[k] == x))
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True
    )
