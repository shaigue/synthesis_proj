import json
from pathlib import Path
from typing import Any, Dict, List

import config
from src.test_utils.positive_state_extractor import collect_positive_states_from_file


def load_test_positive_states(test_dir: Path) -> List[Dict[str, Any]]:
    program_file = next(iter(test_dir.glob('*.py')))
    return collect_positive_states_from_file(program_file)


def load_test_negative_states(test_dir: Path) -> List[Dict[str, Any]]:
    negative_states_path = test_dir / 'negative_states.json'
    if not negative_states_path.exists():
        return []

    with negative_states_path.open('r') as f:
        negative_states = json.load(f)

    return negative_states


def load_test_logic(test_dir: Path) -> None:
    logic_path = test_dir / 'logic.json'
    with logic_path.open('r') as f:
        logic = json.load(f)
    return logic


def load_test(test_dir: Path) -> Dict:
    return {
        'states': {
            '+': load_test_positive_states(test_dir),
            '-': load_test_negative_states(test_dir)
        },
        'logic': load_test_logic(test_dir)
    }


def iter_tests():
    for test_type_dir in config.TESTS_DIR.iterdir():
        if test_type_dir.is_dir():
            test_type = test_type_dir.name
            for test_dir in test_type_dir.iterdir():
                test_name = test_dir.name
                positive_states = load_test_positive_states(test_dir)
                negative_states = load_test_negative_states(test_dir)
                yield {
                    'test_type': test_type,
                    'test_name': test_name,
                    'positive_states': positive_states,
                    'negative_states': negative_states,
                }


def example():
    for x in iter_tests():
        print(x)


if __name__ == '__main__':
    example()
