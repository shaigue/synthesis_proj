import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from src.test_utils.positive_state_extractor import collect_positive_states_from_file


def _load_test_positive_states(test_dir: Path) -> List[Dict[str, Any]]:
    program_file = next(iter(test_dir.glob('*.py')))
    return collect_positive_states_from_file(program_file)


def _load_test_negative_states(test_dir: Path) -> List[Dict[str, Any]]:
    negative_states_path = test_dir / 'negative_states.json'
    if not negative_states_path.exists():
        return []

    with negative_states_path.open('r') as f:
        negative_states = json.load(f)

    return negative_states


def _load_test_logic(test_dir: Path) -> Dict[str, Any]:
    logic_path = test_dir / 'logic.json'
    with logic_path.open('r') as f:
        logic = json.load(f)
    return logic


@dataclass
class SynthesizerTest:
    program: str
    positive_states: List[Dict[str, Any]]
    negative_states: List[Dict[str, Any]]
    safety_property: str
    is_correct: bool
    exists_loop_invariant: bool


def load_test(test_dir: Path) -> SynthesizerTest:
    program = (test_dir / 'program.py').read_text()
    logic = _load_test_logic(test_dir)
    return SynthesizerTest(
        program=program,
        positive_states=_load_test_positive_states(test_dir),
        negative_states=_load_test_negative_states(test_dir),
        safety_property=logic['property'],
        is_correct=logic['holds'],
        exists_loop_invariant=logic['exists_loop_invariant']
    )
