from pathlib import Path
from typing import Dict, Any, List, Optional, Set

from z3 import Solver, And, Not, sat, BoolRef

from src.enumeration import find_loop_invariant
from src.grammar.integers import IntegerParser
from src.test_utils.test_utils import load_test

import config


def run_test(test_dir: Path):
    test_data = load_test(test_dir)
    positive_states = test_data['states']['+']
    negative_states = test_data['states']['-']

    variables = _get_variables(positive_states + negative_states)
    parser = IntegerParser(variables, config.MIN_NUM, config.MAX_NUM)

    property_z3 = parser.compile_to_z3(test_data['logic']['property'])

    for counter_example_round_i in range(config.MAX_COUNTER_EXAMPLES_ROUNDS):
        loop_invariant = find_loop_invariant(parser.grammar, positive_states, negative_states)
        loop_invariant_z3 = parser.compile_to_z3(loop_invariant)
        counter_example = _find_counter_example(loop_invariant_z3, property_z3, variables, default_value=0)
        if counter_example is not None:
            negative_states.append(counter_example)
        else:
            print("loop invariant found")
            return loop_invariant

    print("Failed to find loop invariant")


def _find_counter_example(a: BoolRef, b: BoolRef, variables: Set[str], default_value: Any) -> Optional[Dict[str, Any]]:
    s = Solver()
    s.add(And(a, Not(b)))
    res = s.check()

    if res == sat:
        counter_example = {var: default_value for var in variables}
        model = s.model()
        for model_var in model:
            model_var_name = str(model_var)
            if model_var_name not in variables:
                continue
            value = model[model_var]
            value = value.as_long()
            counter_example[model_var_name] = value

        return counter_example


def _get_variables(states: List[Dict[str, Any]]):
    variables = set(states[0].keys())
    for state in states:
        variables.intersection_update(state.keys())
    return variables


def run_integer_tests():
    integer_tests_dir = config.TESTS_DIR / 'integers'
    for test_dir in integer_tests_dir.iterdir():
        loop_invariant = run_test(test_dir)
        print(loop_invariant)


if __name__ == '__main__':
    run_integer_tests()
