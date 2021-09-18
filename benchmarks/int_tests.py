from z3 import Ints, Or, And, Context

from src.test_utils.benchmark import Benchmark


def test_0():
    def program(x: int, y: int):
        z = max(x, y)
        w = min(x, y)
        while w <= z:
            yield locals()
            w += 1
            z -= 1

    x, y, z, w = Ints('x y z w')
    safety_property = x + y == z + w
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True
    )


def test_1():
    def program(x: int):
        y = 0
        z = 0
        while x > 0:
            yield locals()
            y = x + 1
            z += y
            x -= 1

    def input_condition(x: int):
        return x > 0

    x, y, z = Ints('x y z')
    safety_property = Or(y == 0, And(y > x, z > x))
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )


def test_2():
    def program(x: int, y: int, z: int):
        sign = 1 if x + y + z > 0 else -1
        temp = 0

        if sign == 1:
            x = abs(x)
            y = abs(y)
            z = abs(z)

        else:
            x = - abs(x)
            y = - abs(y)
            z = - abs(z)

        while x != 0 and y != 0 and z != 0:
            yield locals()
            temp = (x - sign)
            x = - y
            y = - z
            z = - temp
            sign = - sign

    def input_condition(x: int, y: int, z: int):
        return x != 0 or y != 0 or z != 0

    ignore_vars = {'temp'}
    x, y, z = Ints('x y z')
    safety_property = Or(
        And(x >= 0, y >= 0, z >= 0),
        And(x <= 0, y <= 0, z <= 0)
    )
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition,
        ignore_vars=ignore_vars
    )


def test_3():
    def program(x: int, y: int):
        i = min(x, y)
        m = max(x, y)
        while i < 2 * m:
            yield locals()
            i += 1

    def input_condition(x: int, y: int):
        return x != y

    x, y, i, m = Ints('x y i m')
    safety_property = Or(i <= 2 * x, i <= 2 * y)
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True,
        input_condition=input_condition
    )


def test_4():
    def program(x: int, y: int):
        # calculates v = x * y
        v = 0
        i = 0
        while i < y:
            yield locals()
            i += 1
            v += x

    def input_condition(x: int, y: int):
        return x > 0 and y > 0

    x, y, v = Ints('x y v')
    safety_property = v <= x * y

    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=False,
        input_condition=input_condition
    )


def test_5():
    def program(x: int, y: int):
        # counts the number of odd numbers between 2 numbers, but it has a bug in it and it counts every number twice
        c = 0
        i = min(x, y)
        m = max(x, y)
        while i <= m:
            yield locals()
            if i % 2 == 1:
                c += 1
                c += 1  # BUG!!!
            i += 1

    def input_condition(x: int, y: int) -> bool:
        return x != y

    x, y, c = Ints('x y c')
    safety_property = Or(
        # if x and y are different then there is at least 1 odd number between them, but it cannot be that all are odd
        And(x > y, c < x - y + 1),
        And(x < y, c < y - x + 1),
        And(x == y, c >= 0, c <= 1)
    )
    return Benchmark(
        program,
        safety_property,
        is_correct=False,
        is_expressible=False,
        input_condition=input_condition
    )

