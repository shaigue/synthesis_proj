import ast
import json
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


def collect_positive_states(program_ast: ast.AST) -> list[dict[str, int]]:
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

# TODO - make a function that generates random string and random lists.


def collect_states(program_ast: ast.AST) -> tuple[list[dict[str, int]], list[dict[str, int]]]:
    positive_states = collect_positive_states(program_ast)
    negative_states = collect_negative_states_randomly(positive_states)
    return positive_states, negative_states


def create_states_for_all_tests():
    tests_dir = config.ROOT_PATH / 'tests'
    for program_path in tests_dir.rglob('program.py'):
        program_ast = ast.parse(program_path.read_text())
        positive_states, negative_states = collect_states(program_ast)
        positive_states_path = program_path.parent / 'positive_states.json'
        with positive_states_path.open('w') as f:
            json.dump(positive_states, f, indent=4)
        negative_states_path = program_path.parent / 'negative_states.json'
        with negative_states_path.open('w') as f:
            json.dump(negative_states, f, indent=4)


if __name__ == '__main__':
    create_states_for_all_tests()
