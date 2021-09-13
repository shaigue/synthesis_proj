from threading import Thread

import config
from src.test_utils.benchmark import Benchmark
from src.library import get_functions_and_constants
from src.synthesis import counter_example_synthesis
from tests import int_tests, str_tests, arr_tests


# TODO: be able to write to output the name of the test
# TODO: take into account in the report the fact that a loop invariant might not be expressible, or incorrect
def run_test(test: Benchmark) -> None:
    positive_examples = test.generate_positive_states(config.N_INPUTS)
    functions, constants = get_functions_and_constants(positive_examples)
    loop_invariant = counter_example_synthesis(positive_examples, functions, constants,
                                               test.safety_property)
    if loop_invariant is None:
        print(f"***loop invariant not found***")
    else:
        print(f"***loop invariant found***\n{loop_invariant}")
    # TODO: write out to file, and save data


def run_tests(tests_module, timeout: int = 5):
    # TODO: some tests might randomly fail do to weird z3 stuff, make sure to elegantly capture that
    test_names = filter(lambda attr_name: attr_name.startswith('test_'), dir(tests_module))
    for test_name in test_names:
        test: Benchmark = getattr(tests_module, test_name)()
        print(f"***running test {test_name} in {tests_module.__name__}***")
        process = Thread(target=run_test, args=(test,))
        process.start()
        # process.join(timeout)
        process.join()
        if process.is_alive():
            print(f"***{test_name} timed out***")


def _test():
    from tests.str_tests import test_1
    run_test(test_1())
    # run_tests(int_tests)


if __name__ == '__main__':
    _test()
