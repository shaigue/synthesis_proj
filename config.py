from pathlib import Path

ROOT_PATH = Path().absolute()
while ROOT_PATH.name != "synthesis_proj":
    ROOT_PATH = ROOT_PATH.parent

TESTS_DIR = ROOT_PATH / 'tests'

MIN_NUM = 0
MAX_NUM = 5
MAX_COUNTER_EXAMPLES_ROUNDS = 10
ARRAY_LEN = 5
