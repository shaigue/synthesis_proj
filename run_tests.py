from pathlib import Path
from datetime import datetime

import config
from src.test_utils.test_utils import load_positive_examples_and_safety_property
from src.library import get_int_functions_and_constants, get_string_functions_and_constants, get_array_functions_and_constants
from src.synthesis import counter_example_synthesis


def run_tests(tests_dir: Path, functions, constants):
    for test_dir in tests_dir.iterdir():
        if not test_dir.is_dir():
            continue
        print(f"running test {test_dir}...")
        positive_examples, safety_property = load_positive_examples_and_safety_property(test_dir)
        loop_invariant = counter_example_synthesis(positive_examples, functions, constants,
                                                   safety_property)
        if loop_invariant is None:
            print(f"***Loop invariant not found***")
        else:
            print(f"***loop_invariant found:{loop_invariant}***")


def run_integer_tests():
    tests_dir = config.TESTS_DIR / 'integers'
    functions, constants = get_int_functions_and_constants()
    run_tests(tests_dir, functions, constants)


def run_string_tests():
    tests_dir = config.TESTS_DIR / 'strings'
    functions, constants = get_string_functions_and_constants()
    run_tests(tests_dir, functions, constants)


def run_array_tests():
    tests_dir = config.TESTS_DIR / 'arrays'
    functions, constants = get_array_functions_and_constants()
    run_tests(tests_dir, functions, constants)


if __name__ == '__main__':
    print(datetime.now())
    # run_integer_tests()
    # run_string_tests()
    run_array_tests()
    print(datetime.now())
