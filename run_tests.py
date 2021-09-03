import config
from src.test_utils.test_utils import load_positive_examples_and_safety_property
from src.library import get_int_functions_and_constants, get_string_functions_and_constants
from src.synthesis import counter_example_synthesis


def run_integer_tests():
    tests_dir = config.TESTS_DIR / 'integers'
    for test_dir in tests_dir.iterdir():
        print(f"running test {test_dir}...")
        positive_examples, safety_property = load_positive_examples_and_safety_property(test_dir)
        functions, constants = get_int_functions_and_constants()
        loop_invariant = counter_example_synthesis(positive_examples, functions, constants,
                                                   safety_property)

        print(f"***loop_invariant found:{loop_invariant}***")


if __name__ == '__main__':
    run_integer_tests()