# TODO:
from z3 import String, Int, Length, Strings, And, PrefixOf, SuffixOf

from src.test_utils.benchmark import Benchmark


def test_0():
    def program(x: int):
        x = abs(x)
        s = ""
        i = 1
        while i < x:
            yield locals()
            i = i + 1
            s = s + "a"

    def input_condition(x: int):
        return x >= 0

    s = String('s')
    x = Int('x')
    safety_property = Length(s) <= x
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )


def test_1():
    def program(s: str, x: int):
        i = 2
        s1 = s[:i]
        s2 = s[i:]
        while x > 0:
            yield locals()
            x = x - 1
            s = 'x' + s + 'y'
            s1 = 'x' + s1
            s2 = s2 + 'y'

    def input_condition(s: str, x: int):
        return len(s) >= 2 and x >= 1

    s, s1, s2 = Strings('s s1 s2')
    safety_property = And(PrefixOf(s1, s), SuffixOf(s2, s))
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )


