# TODO - module to load test data
import json
from pathlib import Path
import ast


def read_program_to_ast(program_path: Path) -> ast.AST:
    source = program_path.read_text()
    return ast.parse(source)


def read_logic_to_dict(logic_path: Path) -> dict:
    with logic_path.open('r') as f:
        return json.load(f)


def main():
    import config
    test_dir = config.ROOT_PATH / 'tests' / 'basic_integer_tests' / '0'

    program_path = test_dir / 'program.py'
    tree = read_program_to_ast(program_path)
    print("AST:")
    print(tree)

    logic_path = test_dir / 'logic.json'
    logic_dict = read_logic_to_dict(logic_path)
    print("Logic:")
    print(logic_dict)


if __name__ == '__main__':
    main()
