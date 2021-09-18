from pathlib import Path

ROOT_PATH = Path().absolute()
while ROOT_PATH.name != "synthesis_proj":
    ROOT_PATH = ROOT_PATH.parent

TESTS_DIR = ROOT_PATH / 'benchmarks'
TESTS_RESULT_DIR = ROOT_PATH / 'tests_results'
if not TESTS_RESULT_DIR.is_dir():
    TESTS_RESULT_DIR.mkdir()

MAX_COUNTER_EXAMPLES_ROUNDS = 40
N_INPUTS = 5
MAX_DEPTH = 3
MIN_ARR_LEN = 0
MAX_ARR_LEN = 5
MIN_STR_LEN = 0
MAX_STR_LEN = 5
MIN_STR_CHAR_ORD = ord('A')
MAX_STR_CHAR_ORD = ord('C')
MIN_INT_VALUE = -10
MAX_INT_VALUE = 10
TEST_TIME_LIMIT_SECONDS = 300
