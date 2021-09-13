"""
Each test should instantiate this class
"""
from copy import deepcopy
from typing import Callable, List, Dict, Any, Iterator

from z3 import BoolRef

from src.test_utils.input_generation import generate_inputs_for_program


class Benchmark:
    def __init__(self, program: Callable[..., Iterator[Dict[str, Any]]], safety_property: BoolRef,
                 is_correct: bool, is_expressible: bool, input_condition: Callable[..., bool] = None):
        assert not is_expressible or is_correct, f"If expressible, must be correct, got is_correct={is_correct}," \
                                                 f" is_expressible={is_expressible}"
        self.program = program
        self.safety_property = safety_property
        self.is_correct = is_correct
        self.is_expressible = is_expressible
        self.input_condition = input_condition

    def generate_positive_states(self, n_inputs: int) -> List[Dict[str, Any]]:
        positive_states = []
        for i in range(n_inputs):
            inputs = generate_inputs_for_program(self.program, self.input_condition)
            for state in self.program(**inputs):
                state = deepcopy(state)
                positive_states.append(state)
        return positive_states

