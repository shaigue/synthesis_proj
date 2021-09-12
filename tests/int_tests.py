from z3 import Ints, Or, And

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
        if x < 0:
            x = - x
        y = 0
        z = 0
        while x > 0:
            yield locals()
            y = x + 1
            z += y
            x -= 1

    x, y, z = Ints('x y z')
    safety_property = Or(y == 0, And(y > x, z > x))
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True
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

    x, y, z = Ints('x y z')
    safety_property = Or(
        And(x >= 0, y >= 0, z >= 0),
        And(x <= 0, y <= 0, z <= 0)
    )
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True
    )
