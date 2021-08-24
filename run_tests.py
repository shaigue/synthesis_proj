from pathlib import Path

from z3 import Solver, And, Not, sat

from src.enumeration import find_loop_invariant
from src.grammar.integers import compile_exp_text_to_z3, get_grammar_string
from src.test_utils.test_utils import load_test

import config


def run_test(test_dir: Path):
    # TODO - find out what variables appear in all of the states, and put them inside of the grammar
    #   and give them default values in the counter examples generation
    test_data = load_test(test_dir)
    positive_states = test_data['states']['+']
    negative_states = test_data['states']['-']

    variables = set(positive_states[0].keys())
    for state in positive_states:
        variables.intersection_update(state.keys())

    property_z3 = compile_exp_text_to_z3(test_data['logic']['property'])

    max_attempts = 20
    for attempt_i in range(max_attempts):
        loop_invariant = find_loop_invariant(get_grammar_string(), positive_states, negative_states)
        loop_invariant_z3 = compile_exp_text_to_z3(loop_invariant)
        s = Solver()
        s.add(And(loop_invariant_z3, Not(property_z3)))
        res = s.check()
        if res == sat:
            model = s.model()
            negative_example = {}
            for variable in model:
                variable_name = str(variable)
                if variable_name not in variables:
                    continue
                value = model[variable]
                value = value.as_long()
                negative_example[variable_name] = value

            negative_states.append(negative_example)
        else:
            print("found invariant!!!")
            print(loop_invariant)
            return 0
    print("failed to find invariant!!!")
    return 1


def run_integer_tests():
    integer_tests_dir = config.TESTS_DIR / 'integers'
    for test_dir in integer_tests_dir.iterdir():
        run_test(test_dir)
    # parse the safety property into z3 formula
    # load the positive and negative samples
    # synthesis a loop invariant for those samples
    # parse the loop invariant into z3 formula
    # check if (loop invariant => safety property) if so, we are done, else add the negative example and run again
    # save the loop invariant to a file
    pass


if __name__ == '__main__':
    run_integer_tests()
