"""This file defines the grammar for integers, and formula translation from python expressions to Z3 formulas"""
from typing import Union, Set

from z3 import BoolRef, ArithRef, And, Or, Int

from adt.tree import Tree
from parsing.earley.grammar import Grammar
from src.generic_parser import GenericParser


class IntegerParser:
    def __init__(self, variables: Set[str], min_num: int, max_num: int):
        grammar_str = _get_grammar_str(variables, min_num, max_num)
        tokens_str = _get_tokens_str(variables, min_num, max_num)
        self.grammar = Grammar.from_string(grammar_str)
        self.parser = GenericParser(tokens_str, grammar_str)

    def _parse_py_expr(self, py_expr: str) -> Tree:
        parse_trees = self.parser(py_expr)
        if parse_trees is None:
            raise RuntimeError(f"got invalid expression {py_expr}")
        return parse_trees.nodes[0].subtrees[0]

    def compile_to_z3(self, py_expr: str) -> BoolRef:
        tree = self._parse_py_expr(py_expr)
        return _logic_expr_to_z3(tree)


def _get_num_str(min_num: int, max_num: int) -> str:
    return "|".join(map(str, range(min_num, max_num + 1)))


def _get_var_str(variables: Set[str]) -> str:
    return "|".join(variables)


def _get_grammar_str(variables: Set[str], min_num: int, max_num: int) -> str:
    numbers_str = _get_num_str(min_num, max_num)
    variables_str = _get_var_str(variables)

    return "\n".join([
        "LEXPR -> ( AEXPR RELOP AEXPR ) | ( LEXPR LOP LEXPR )",
        "AEXPR -> VAR | AEXPR AOP AEXPR | NUM",
        "NUM -> " + numbers_str,
        "VAR -> " + variables_str,
        "RELOP -> == | != | < | <=",
        "LOP -> and | or",
        "AOP -> + | - | * "
    ])


def _get_tokens_str(variables: Set[str], min_num: int = 0, max_num: int = 5) -> str:
    return r"<=|<|!=|==|and|or|\)|\(|\+|-|\*" + '|' + _get_var_str(variables) + '|' + _get_num_str(min_num, max_num)


def _logic_expr_to_z3(tree: Tree) -> BoolRef:
    assert tree.root == "LEXPR"

    _, expr1, op_node, expr2, _ = tree.subtrees
    op = op_node.leaves[0].func

    if op_node.func == "RELOP":
        expr1 = _arith_expr_to_z3(expr1)
        expr2 = _arith_expr_to_z3(expr2)
        if op == "==":
            return expr1 == expr2
        if op == "!=":
            return expr1 != expr2
        if op == "<":
            return expr1 < expr2
        if op == "<=":
            return expr1 <= expr2

    if op_node.func == "LOP":
        expr1 = _logic_expr_to_z3(expr1)
        expr2 = _logic_expr_to_z3(expr2)
        if op == "and":
            return And(expr1, expr2)
        if op == "or":
            return Or(expr1, expr2)


def _arith_expr_to_z3(tree: Tree) -> Union[ArithRef, int]:
    assert tree.root == "AEXPR"

    if len(tree.subtrees) == 1:
        terminal = tree.leaves[0].func
        if terminal.isnumeric():
            return int(terminal)
        else:
            return Int(terminal)

    else:
        expr1, op, expr2 = tree.subtrees
        expr1 = _arith_expr_to_z3(expr1)
        expr2 = _arith_expr_to_z3(expr2)
        op = op.leaves[0].func
        if op == '+':
            return expr1 + expr2
        if op == '-':
            return expr1 - expr2
        if op == '*':
            return expr1 * expr2
        if op == '//':
            return expr1 // expr2
        if op == '%':
            return expr1 % expr2


def main():
    exp_text = "( ( ( x <= y ) or ( z < 3 ) ) and ( 1 < x ) )"
    grammar_str = _get_grammar_str({'x', 'y', 'w'}, 0, 4)
    tokens_str = _get_tokens_str({'x', 'y', 'w'}, 0, 4)
    print(grammar_str)
    print(tokens_str)
    grammar = Grammar.from_string(grammar_str)
    parser = GenericParser(tokens_str, grammar_str)

    exp = "( x + x != 2 % y )"
    x = parser(exp)
    print(x)


if __name__ == '__main__':
    main()
