import logging

import config
from src.test_utils.benchmark import Benchmark
from src.library import get_functions_and_constants
from src.synthesis import counter_example_synthesis
from benchmarks import int_tests, str_tests, int_seq_tests
from datetime import datetime

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)


def run_test(test: Benchmark, timeout: int):
    positive_examples = test.generate_positive_states(config.N_INPUTS)
    functions, constants = get_functions_and_constants(positive_examples)
    result = counter_example_synthesis(positive_examples, functions, constants, test.safety_property,
                                       config.MAX_COUNTER_EXAMPLES_ROUNDS, test.ignore_vars, timeout)
    if result.timeout:
        logging.info("timed-out")
    elif result.bad_property:
        logging.info(f"bad property: {test.safety_property} bad_example: {result.value}")
    else:
        logging.info(f"loop invariant found:\n{result.value}")
    return result


def run_tests(tests_module, timeout=config.TEST_TIME_LIMIT_SECONDS):
    test_names = filter(lambda attr_name: attr_name.startswith('test_'), dir(tests_module))
    test_module_name = tests_module.__name__.split('.')[-1]
    group_result_file = config.TESTS_RESULT_DIR / f'{test_module_name}.txt'
    columns = ["result", "runtime", "is correct", "is expressible"]
    row_format = "{:<15}" * (len(columns) + 1)
    with group_result_file.open("w") as f:
        f.write(row_format.format("", *columns))
        f.write("\n")
    for test_name in test_names:
        test: Benchmark = getattr(tests_module, test_name)()
        logging.info(f"running test {test_name} in {test_module_name}")
        logging.info(f"correct={test.is_correct}, expressible={test.is_expressible}")

        start = datetime.now()
        result = run_test(test, timeout)
        logging.info(f"Time:{datetime.now() - start}")

        result_file = config.TESTS_RESULT_DIR / f'{test_module_name}_{test_name}.txt'
        with result_file.open('w') as f_test:
            with group_result_file.open('a') as f_group:
                if result.timeout:
                    f_test.write("TIMEOUT")
                    f_group.write(row_format.format(test_name, "timeout", round(result.runtime, 4), test.is_correct, test.is_expressible))
                    f_group.write("\n")
                elif result.bad_property:
                    f_test.write(f"BAD PROPERTY: {test.safety_property} WITH POSITIVE EXAMPLE: {result.value}")
                    f_group.write(row_format.format(test_name, "bad property", round(result.runtime, 4), test.is_correct, test.is_expressible))
                    f_group.write("\n")
                else:
                    f_test.write(str(result.value))
                    f_group.write(row_format.format(test_name, "success", round(result.runtime, 4), test.is_correct, test.is_expressible))
                    f_group.write("\n")


def _test():
    # from benchmarks.int_tests import test_0, test_1, test_2, test_3, test_4, test_5
    # from benchmarks.str_tests import test_0, test_1, test_2, test_3, test_4, test_5
    # from benchmarks.int_seq_tests import test_0, test_1, test_2, test_3, test_4, test_5

    # run_test(test_2(), 200)
    # run_test(test_5(), 200)

    run_tests(int_tests)
    run_tests(str_tests)
    run_tests(int_seq_tests)


if __name__ == '__main__':
    _test()
