# TODO - collect also negative examples

import ast
from _ast import While, Module
from typing import Any

import config


class CollectLoopStatesTransformer(ast.NodeTransformer):
    def visit_While(self, node: While) -> Any:
        # TODO: change this to support other types of variables
        states_append_stmt = "_states.append(dict(filter(lambda v: isinstance(v[1], int), locals().items())))"
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


def collect_positive_states(program_ast: ast.Module) -> list[dict]:
    transformed_ast = CollectLoopStatesTransformer().visit(program_ast)
    transformed_ast = ast.fix_missing_locations(transformed_ast)
    transformed_code = compile(transformed_ast, filename='<string>', mode='exec')
    exec(transformed_code)
    return locals()['_states']


def example():
    strip_src = """
    x = 1
    n = 10
    while n > 0:
        n = n - 1
    """
    print(collect_positive_states(ast.parse(strip_src)))


def try_on_all_tests():
    tests_dir = config.ROOT_PATH / 'tests'
    for program_path in tests_dir.rglob('program.py'):
        program_ast = ast.parse(program_path.read_text())
        positive_states = collect_positive_states(program_ast)
        print(f'{program_path}\n{positive_states}')


if __name__ == '__main__':
    example()
    try_on_all_tests()
