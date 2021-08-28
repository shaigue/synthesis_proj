from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from enum import Enum
from datetime import datetime

from z3 import Solver, And, Not, sat, BoolRef

from src.enumeration import find_loop_invariant
from src.grammar.integers import IntegerParser
from src.grammar.strings import StringParser
from src.test_utils.test_utils import load_test

import config


class TestType(Enum):
    INTEGER = 1
    STRING = 2


def get_parser(test: TestType, variables):
    if test == TestType.INTEGER:
        return IntegerParser(variables, config.MIN_NUM, config.MAX_NUM)
    elif test == TestType.STRING:
        return StringParser({v for v in variables if not v.startswith('s')},
                            {v for v in variables if v.startswith('s')}, config.MIN_NUM, config.MAX_NUM)
    else:
        assert False


def run_test(test_dir: Path, test: TestType):
    test_data = load_test(test_dir)
    positive_states = test_data['states']['+']
    negative_states = test_data['states']['-']

    variables = _get_variables(positive_states + negative_states)
    # parser = IntegerParser(variables, config.MIN_NUM, config.MAX_NUM)
    parser = get_parser(test, variables)

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
            try:
                value = value.as_long()
            except AttributeError:
                value = value.as_string()
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
        loop_invariant = run_test(test_dir, TestType.INTEGER)
        print(loop_invariant)


def run_string_tests():
    integer_tests_dir = config.TESTS_DIR / 'strings'
    for test_dir in integer_tests_dir.iterdir():
        loop_invariant = run_test(test_dir, TestType.STRING)
        print(loop_invariant)
        print(datetime.now())


if __name__ == '__main__':
    # print(datetime.now())
    # run_integer_tests()
    print(datetime.now())
    run_string_tests()
