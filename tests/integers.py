from z3 import Ints

from src.test_utils.benchmark import Benchmark

# TODO: convert tests to new format
# TODO: delete collect states stuff
# TODO: deal with the _store issue
def test_0():
    def program():
        pass

    x, y = Ints('x y')
    safety_property = x > y
    return Benchmark(
        program,
        safety_property,
        is_correct=True,
        is_expressible=True
    )
