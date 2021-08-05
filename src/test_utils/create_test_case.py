import json
import sys

import config

if len(sys.argv) != 2:
    print("should be run with 'create_test_case.py <test_type>'")
    exit(1)

test_type = sys.argv[1]
test_type_dir = config.ROOT_PATH / 'tests' / test_type
test_type_dir.mkdir(parents=True, exist_ok=True)
n_existing_tests = len(list(test_type_dir.glob('*')))
new_test_dir = test_type_dir / f'{n_existing_tests}'
new_test_dir.mkdir()
(new_test_dir / 'program.py').touch()
(new_test_dir / 'negative_states.json').touch()
(new_test_dir / 'positive_states.json').touch()
logic_dict = {"precondition": "", "postcondition": "", "loop_invariant": "", "correct": True}
with open(new_test_dir / 'logic.json', 'w') as f:
    json.dump(logic_dict, f, indent=4)

