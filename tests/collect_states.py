import ast
from _ast import While, Module
from typing import Any
import random

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


def collect_positive_states(program_ast: ast.Module) -> list[dict[str, int]]:
    transformed_ast = CollectLoopStatesTransformer().visit(program_ast)
    transformed_ast = ast.fix_missing_locations(transformed_ast)
    transformed_code = compile(transformed_ast, filename='<string>', mode='exec')
    exec(transformed_code)
    return locals()['_states']


def collect_negative_states_randomly(positive_states: list[dict[str, int]], n_states: int = 5) -> list[dict[str, int]]:
    # TODO: after that the generation of the predicate is complete, we can rank randomly generated states by how
    #   much simple the term gets when adding them, or in some other way.
    #   the idea is that the negative samples are also something that can be "synthesized", until the property is
    #   proved. if this doesn't work just manually add negative states
    # TODO: allow types other then integers
    variables = set()
    for state in positive_states:
        variables.update(state.keys())
    negative_states = []
    while len(negative_states) < n_states:
        state = {}
        for v in variables:
            state[v] = random.randint(-100, 100)
        if state not in positive_states and state not in negative_states:
            negative_states.append(state)
    return negative_states


EXAMPLE_SRC = """
x = 1
n = 10
while n > 0:
    n = n - 1
"""


def positive_example():
    print(collect_positive_states(ast.parse(EXAMPLE_SRC)))


def try_on_all_tests():
    tests_dir = config.ROOT_PATH / 'tests'
    for program_path in tests_dir.rglob('program.py'):
        program_ast = ast.parse(program_path.read_text())
        positive_states = collect_positive_states(program_ast)
        negative_states = collect_negative_states_randomly(positive_states)
        print(f'{program_path}\nPOSITIVE={positive_states}\nNEGATIVE={negative_states}')


if __name__ == '__main__':
    positive_example()
    try_on_all_tests()
