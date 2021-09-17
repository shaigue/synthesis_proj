from pathlib import Path

ROOT_PATH = Path().absolute()
while ROOT_PATH.name != "synthesis_proj":
    ROOT_PATH = ROOT_PATH.parent

TESTS_DIR = ROOT_PATH / 'benchmarks'

MAX_COUNTER_EXAMPLES_ROUNDS = 40
N_INPUTS = 10
MAX_DEPTH = 4
MIN_ARR_LEN = 0
MAX_ARR_LEN = 5
MIN_STR_LEN = 0
MAX_STR_LEN = 5
MIN_STR_CHAR_ORD = ord('A')
MAX_STR_CHAR_ORD = ord('C')
MIN_INT_VALUE = -10
MAX_INT_VALUE = 10
