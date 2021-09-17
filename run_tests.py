import logging

import config
from src.test_utils.benchmark import Benchmark
from src.library import get_functions_and_constants
from src.synthesis import counter_example_synthesis
from benchmarks import int_tests, str_tests, int_seq_tests
from datetime import datetime

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

# TODO: check that the negative examples work well
# TODO: take into account in the report the fact that a loop invariant might not be expressible, or incorrect
def run_test(test: Benchmark) -> None:
    # TODO: write out to file, and save data
    # TODO: remove this to show failure
    if not test.is_correct or not test.is_expressible:
        logging.info(f"skipping unprovable test")
        return

    positive_examples = test.generate_positive_states(config.N_INPUTS)
    functions, constants = get_functions_and_constants(positive_examples)
    result = counter_example_synthesis(positive_examples, functions, constants, test.safety_property,
                                       config.MAX_COUNTER_EXAMPLES_ROUNDS, test.ignore_vars)
    if result.timeout:
        logging.info("timed-out")
    elif result.bad_property:
        logging.info(f"bad property: {test.safety_property} bad_example: {result.value}")
    else:
        logging.info(f"loop invariant found:\n{result.value}")


def run_tests(tests_module):
    # TODO: some tests might randomly fail do to weird z3 stuff, make sure to elegantly capture that
    test_names = filter(lambda attr_name: attr_name.startswith('test_'), dir(tests_module))
    for test_name in test_names:
        start = datetime.now()
        test: Benchmark = getattr(tests_module, test_name)()

        logging.info(f"running test {test_name} in {tests_module.__name__}")
        run_test(test)
        # logging.info(f"Time:{datetime.now() - start}")


def _test():
    # from benchmarks.int_tests import test_0, test_1, test_2, test_3, test_4, test_5
    # from benchmarks.str_tests import test_0, test_1, test_2, test_3, test_4, test_5
    from benchmarks.int_seq_tests import test_0, test_1, test_2, test_3, test_4, test_5

    # run_test(test_3())
    #
    run_tests(int_tests)
    run_tests(str_tests)
    run_tests(int_seq_tests)


if __name__ == '__main__':
    _test()
