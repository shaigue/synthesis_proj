"""
Input: a python program as a file with strings / ints / lists and a single while loop
Output: list of states that occur at the start of the loop
"""

# TODO: shai, implement

import ast
from _ast import While, Module
from pathlib import Path
from typing import Any, List, Dict

import config


class CollectLoopStatesTransformer(ast.NodeTransformer):
    def visit_While(self, node: While) -> Any:
        states_append_stmt = "_states.append(dict(filter(lambda v: not v[0].startswith('_'), locals().items())))"
        states_append_subtree = ast.parse(states_append_stmt).body[0]
        body = node.body.copy()
        body.insert(0, states_append_subtree)
        return While(
            test=node.test,
            body=body,
            orelse=node.orelse,
        )

    def visit_Module(self, node: Module) -> Any:
        body = [self.visit(subtree) for subtree in node.body]
        states_declare_stmt = '_states = []'
        states_declare_subtree = ast.parse(states_declare_stmt).body[0]
        body.insert(0, states_declare_subtree)
        return Module(
            body=body,
            type_ignores=node.type_ignores,
        )


def collect_positive_states_from_ast(program_ast: ast.AST) -> List[Dict[str, Any]]:
    transformed_ast = CollectLoopStatesTransformer().visit(program_ast)
    transformed_ast = ast.fix_missing_locations(transformed_ast)
    transformed_code = compile(transformed_ast, filename='<string>', mode='exec')
    local_vars = {}
    exec(transformed_code, {}, local_vars)
    return local_vars['_states']


def collect_positive_states_from_file(program_file: Path) -> List[Dict[str, Any]]:
    program_ast = ast.parse(program_file.read_text())
    return collect_positive_states_from_ast(program_ast)


def collect_positive_states_from_all_tests():
    for program_file in config.TESTS_DIR.rglob('*.py'):
        positive_states = collect_positive_states_from_file(program_file)
        print(f'test file: {program_file}')
        print(f'positive states:')
        print(positive_states)


if __name__ == '__main__':
    collect_positive_states_from_all_tests()
