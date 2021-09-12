"""
Each test should instantiate this class
"""
from typing import Callable

from z3 import BoolRef


class Benchmark:
    def __init__(self, program: Callable, safety_property: BoolRef, is_correct, is_expressible):
        assert not is_expressible or is_correct, f"If expressible, must be correct, got is_correct={is_correct}," \
                                                 f" is_expressible={is_expressible}"
        self.program = program
        self.safety_property = safety_property
        self.is_correct = is_correct
        self.is_expressible = is_expressible
