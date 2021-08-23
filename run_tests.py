from pathlib import Path
from src.test_utils.test_utils import load_test

import config


def run_test(test_dir: Path):
    test_data = load_test(test_dir)
    print("end")


def run_integer_tests():
    # parse the safety property into z3 formula
    # load the positive and negative samples
    # synthesis a loop invariant for those samples
    # parse the loop invariant into z3 formula
    # check if (loop invariant => safety property) if so, we are done, else add the negative example and run again
    # save the loop invariant to a file
    pass


if __name__ == '__main__':
    # run_integer_tests()
    test_dir = config.TESTS_DIR / 'integers' / '0'
    run_test(test_dir)
