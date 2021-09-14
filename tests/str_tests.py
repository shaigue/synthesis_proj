import random

from z3 import String, Int, Length, Strings, And, PrefixOf, SuffixOf, Or, IndexOf, Contains, Concat, Not

from src.test_utils.benchmark import Benchmark


def test_0():
    def program(x: int):
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


def test_2():
    def program(s: str, s1: str, s2: str, t: int):
        i = 0
        j = 0
        s = s1 + s
        while i < t and j < t:
            yield locals()
            if i == j:
                i = i + 1
                s = s2 + s
            else:
                j = j + 1
                s = s1 + s

    def input_condition(s: str, s1: str, s2: str, t: int):
        return len(s) >= 2 and len(s1) >= 2 and len(s2) >= 2 and t >= 0

    s, s1, s2 = Strings('s s1 s2')
    safety_property = Or(PrefixOf(s2, s), PrefixOf(s1, s))

    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )


def test_3():
    def program(x: int, y: int):
        s = "x"
        while x < y:
            yield locals()
            y = y - 1
            s = s + 'a'

    def input_condition(x: int, y: int):
        return 0 < x < y

    s = String('s')
    safety_property = IndexOf(s, 'x') == 0

    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=False,  # it is not expressible since there are no literals in the grammar
        input_condition=input_condition
    )


def test_4():
    def program(s: str, x: int):
        i = 2
        s1 = s[:i]
        s2 = s[i:]
        while x > 0:
            yield locals()
            x = x - 1
            s = 'x' + s + 'y'
            s1 = 'x' + s1
            s2 = 'y' + s2   # BUG, should be s2 + 'y'

    def input_condition(s: str, x: int):
        return len(s) >= 2 and x >= 1

    s, s1, s2 = Strings('s s1 s2')
    safety_property = And(PrefixOf(s1, s), SuffixOf(s2, s))

    return Benchmark(
        program,
        safety_property,
        is_correct=False,
        is_expressible=False,
        input_condition=input_condition
    )


def test_5():
    def program(s: str):
        i = random.randrange(len(s))
        s1 = s[:i]
        s2 = s[i:]
        j = 0
        c = ({'A', 'B', 'C'} - {s[0], s[-1]}).pop()

        while j < i ** 2:
            yield locals()
            if j % 2 == 1:
                s1 = c + s1
            else:
                s2 = s2 + c
            j += 1

    def input_condition(s: str):
        return len(s) > 2

    s, s1, s2 = Strings('s s1 s2')
    cat = Concat(s1, s2)
    safety_property = And(
        Contains(cat, s),
        Not(Contains(s1, s)),
        Not(Contains(s2, s))
    )

    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )
