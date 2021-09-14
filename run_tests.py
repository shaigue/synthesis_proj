import config
from src.test_utils.benchmark import Benchmark
from src.library import get_functions_and_constants
from src.synthesis import counter_example_synthesis
from tests import int_tests, str_tests, int_seq_tests


# TODO: take into account in the report the fact that a loop invariant might not be expressible, or incorrect
def run_test(test: Benchmark) -> None:
    # TODO: write out to file, and save data
    positive_examples = test.generate_positive_states(config.N_INPUTS)
    functions, constants = get_functions_and_constants(positive_examples)
    result = counter_example_synthesis(positive_examples, functions, constants,
                                       test.safety_property)
    if result.timeout:
        print("***timed-out***")
    elif result.bad_property:
        print(f"***bad property: {test.safety_property} bad_example: {result.value}***")
    else:
        print(f"***loop invariant found:***\n{result.value}")


def run_tests(tests_module):
    # TODO: some tests might randomly fail do to weird z3 stuff, make sure to elegantly capture that
    test_names = filter(lambda attr_name: attr_name.startswith('test_'), dir(tests_module))
    for test_name in test_names:
        test: Benchmark = getattr(tests_module, test_name)()
        print(f"***running test {test_name} in {tests_module.__name__}***")
        run_test(test)


def _test():
    from tests.int_seq_tests import test_0
    run_test(test_0())

    # run_tests(int_tests)


if __name__ == '__main__':
    _test()
