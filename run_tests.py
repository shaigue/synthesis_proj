from pathlib import Path
from datetime import datetime
from multiprocessing import Process
import time
from typing import Callable, List

import config
from src.test_utils.test_utils import load_positive_examples_and_safety_property
from src.library import get_int_functions_and_constants, get_string_functions_and_constants, get_array_functions_and_constants
from src.synthesis import counter_example_synthesis


def run_test(test_dir: Path, functions: List[Callable], constants: List) -> None:
    print(f"running test {test_dir}...")
    positive_examples, safety_property = load_positive_examples_and_safety_property(test_dir)
    loop_invariant = counter_example_synthesis(positive_examples, functions, constants,
                                               safety_property)
    if loop_invariant is None:
        print(f"***Loop invariant not found***")
    else:
        print(f"***loop_invariant found:{loop_invariant}***")
    # TODO: write out to file, and save data


def run_tests(tests_dir: Path, functions, constants, timeout: int = 5):
    for test_dir in tests_dir.iterdir():
        if not test_dir.is_dir():
            continue
        process = Process(target=run_test, args=(test_dir, functions, constants))
        process.start()
        # process.join(timeout)
        process.join()
        if process.is_alive():
            print(f"{test_dir} timed out")


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
    # print(datetime.now())
    # run_integer_tests()
    # run_string_tests()
    run_array_tests()
    # print(datetime.now())
