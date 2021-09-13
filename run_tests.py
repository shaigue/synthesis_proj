from threading import Thread
from typing import Callable, List

import config
from src.test_utils.benchmark import Benchmark
from src.library import get_int_functions_and_constants, get_string_functions_and_constants, get_array_functions_and_constants
from src.synthesis import counter_example_synthesis


# TODO: be able to write to output the name of the test
# TODO: take into account in the report the fact that a loop invariant might not be expressible, or incorrect
def run_test(test: Benchmark, functions: List[Callable], constants: List) -> None:
    print(f"running test {test}...")
    positive_examples = test.generate_positive_states(config.N_INPUTS)
    loop_invariant = counter_example_synthesis(positive_examples, functions, constants,
                                               test.safety_property)
    if loop_invariant is None:
        print(f"***Loop invariant not found***")
    else:
        print(f"***loop_invariant found:{loop_invariant}***")
    # TODO: write out to file, and save data


def run_tests(tests_module, functions, constants, timeout: int = 5):
    # TODO: some tests might randomly fail do to weird z3 stuff, make sure to elegantly capture that
    test_names = filter(lambda attr_name: attr_name.startswith('test_'), dir(tests_module))
    for test_name in test_names:
        test: Benchmark = getattr(tests_module, test_name)()
        process = Thread(target=run_test, args=(test, functions, constants))
        process.start()
        # process.join(timeout)
        process.join()
        if process.is_alive():
            print(f"{test_name} timed out")


def run_integer_tests():
    from tests import int_tests
    functions, constants = get_int_functions_and_constants()
    run_tests(int_tests, functions, constants)


def run_string_tests():
    tests_dir = config.TESTS_DIR / 'strings'
    functions, constants = get_string_functions_and_constants()
    run_tests(tests_dir, functions, constants)


def run_array_tests():
    tests_dir = config.TESTS_DIR / 'arrays'
    functions, constants = get_array_functions_and_constants()
    run_tests(tests_dir, functions, constants)


def _test():
    from src.library import get_int_functions_and_constants
    from tests.int_tests import test_5
    functions, constants = get_int_functions_and_constants()
    run_test(test_5(), functions, constants)
    # run_integer_tests()


if __name__ == '__main__':
    _test()
