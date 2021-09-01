import config
from src.test_utils.test_utils import load_test
from src.grammar.str_utils import *

for test_type_dir in config.TESTS_DIR.iterdir():
    print(f"***test type: {test_type_dir.name}***")
    for test_dir in test_type_dir.iterdir():
        print(f"test in dir: {test_dir}")
        test_data = load_test(test_dir)
        for positive_example in test_data.positive_states:
            value = eval(test_data.safety_property, positive_example.copy(), globals())
            if test_data.is_correct and not value:
                print(f"prop: {test_data.safety_property} evaluated false on {positive_example}")
