import json
from pathlib import Path

import config


def load_test_positive_and_negative_states(test_dir: Path):
    positive_states_path = test_dir / 'positive_states.json'
    with positive_states_path.open('r') as f:
        positive_states = json.load(f)
    negative_states_path = test_dir / 'negative_states.json'
    with negative_states_path.open('r') as f:
        negative_states = json.load(f)
    return positive_states, negative_states


def iter_all_positive_and_negative_states():
    tests_dir = config.ROOT_PATH / 'tests'
    for test_type_dir in tests_dir.iterdir():
        if test_type_dir.is_dir():
            test_type = test_type_dir.name
            for test_dir in test_type_dir.iterdir():
                test_name = test_dir.name
                positive_states, negative_states = load_test_positive_and_negative_states(test_dir)
                yield {
                    'test_type': test_type,
                    'test_name': test_name,
                    'positive_states': positive_states,
                    'negative_states': negative_states,
                }


def example():
    for x in iter_all_positive_and_negative_states():
        print(x)


if __name__ == '__main__':
    example()
