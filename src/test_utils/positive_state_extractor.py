"""function to use - collect_positive_states_from_file().

Input: a python program as a file with strings / ints / lists and a single while loop
Output: list of states that occur at the start of the loop
"""
import ast
from _ast import While, Module, FunctionDef
from pathlib import Path
from typing import Any, List, Dict

import config


class _CollectLoopStatesTransformer(ast.NodeTransformer):
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
        # Try except is because we don't know how many args the test function gets
        collect_states_stmt = """
_all_states = []
try:
    for inp in get_inputs():
        _all_states += test(*inp)
except TypeError:
    for inp in get_inputs():
        _all_states += test(inp)
        """
        collect_states_subtrees = ast.parse(collect_states_stmt).body
        body += collect_states_subtrees
        return Module(
            body=body,
            type_ignores=node.type_ignores,
        )

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        if node.name != "test":
            return node
        body = [self.visit(subtree) for subtree in node.body]
        states_declare_stmt = '_states = []'
        states_declare_subtree = ast.parse(states_declare_stmt).body[0]
        body.insert(0, states_declare_subtree)
        states_return_stmt = 'return _states'
        states_return_subtree = ast.parse(states_return_stmt).body[0]
        body.append(states_return_subtree)
        return FunctionDef(
            name=node.name,
            args=node.args,
            body=body,
            decorator_list=node.decorator_list,
            returns=node.returns,
            type_comment=node.type_comment,
        )



def _collect_positive_states_from_ast(program_ast: ast.AST) -> List[Dict[str, Any]]:
    transformed_ast = _CollectLoopStatesTransformer().visit(program_ast)
    transformed_ast = ast.fix_missing_locations(transformed_ast)
    transformed_code = compile(transformed_ast, filename='<string>', mode='exec')
    local_vars = {}
    exec(transformed_code, {}, local_vars)
    return local_vars['_all_states']


def collect_positive_states_from_file(program_file: Path) -> List[Dict[str, Any]]:
    program_ast = ast.parse(program_file.read_text())
    return _collect_positive_states_from_ast(program_ast)


def _collect_positive_states_from_all_tests():
    for program_file in config.TESTS_DIR.rglob('*.py'):
        positive_states = collect_positive_states_from_file(program_file)
        print(f'test file: {program_file}')
        print(f'positive states:')
        print(positive_states)


if __name__ == '__main__':
    _collect_positive_states_from_all_tests()
