"""This file defines the grammar for integers, and formula translation from python expressions to Z3 formulas"""
from typing import Union

from adt.tree import Tree
from parsing.earley.grammar import Grammar
from src.generic_parser import GenericParser
from z3 import BoolRef, ArithRef, And, Or, Int, Solver, sat


def get_grammar_string() -> str:
    return r"""
        LEXPR -> ( AEXPR RELOP AEXPR ) | ( LEXPR LOP LEXPR )
        AEXPR -> VAR | AEXPR AOP AEXPR | NUM
        NUM -> 1 | 2 | 3 | 4 | 5 | 0
        VAR -> x | y | z | temp
        RELOP -> == | != | < | <=
        LOP -> and | or
        AOP -> + | - | * | // | %
    """


def get_tokens_string() -> str:
    return r"x|y|z|<=|<|!=|==|and|or|\)|\(|\+|-|\*|/|0|1|2|3|4|5%"


def get_grammar() -> Grammar:
    return Grammar.from_string(get_grammar_string())


def get_parser() -> GenericParser:
    return GenericParser(get_tokens_string(), get_grammar_string())


def logic_expr_to_z3(tree: Tree) -> BoolRef:
    assert tree.root == "LEXPR"

    _, expr1, op_node, expr2, _ = tree.subtrees
    op = op_node.leaves[0].root

    if op_node.root == "RELOP":
        expr1 = arith_expr_to_z3(expr1)
        expr2 = arith_expr_to_z3(expr2)
        if op == "==":
            return expr1 == expr2
        if op == "!=":
            return expr1 != expr2
        if op == "<":
            return expr1 < expr2
        if op == "<=":
            return expr1 <= expr2

    if op_node.root == "LOP":
        expr1 = logic_expr_to_z3(expr1)
        expr2 = logic_expr_to_z3(expr2)
        if op == "and":
            return And(expr1, expr2)
        if op == "or":
            return Or(expr1, expr2)


def arith_expr_to_z3(tree: Tree) -> Union[ArithRef, int]:
    assert tree.root == "AEXPR"

    if len(tree.subtrees) == 1:
        terminal = tree.leaves[0].root
        if terminal.isnumeric():
            return int(terminal)
        else:
            return Int(terminal)

    else:
        expr1, op, expr2 = tree.subtrees
        expr1 = arith_expr_to_z3(expr1)
        expr2 = arith_expr_to_z3(expr2)
        op = op.leaves[0].root
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


def compile_exp_text_to_z3(exp_text: str) -> BoolRef:
    parser = get_parser()
    tree_with_head = parser(exp_text)
    if tree_with_head is None:
        raise RuntimeError(f"got invalid expression {exp_text}")
    tree = tree_with_head.nodes[0].subtrees[0]
    return logic_expr_to_z3(tree)

    
def main():
    exp_text = "( ( ( x <= y ) or ( z < 3 ) ) and ( 1 < x ) )"
    formula = compile_exp_text_to_z3(exp_text)
    print(formula)
    s = Solver()
    s.add(formula)
    res = s.check()
    if res == sat:
        print(f"model: {s.model()}")


if __name__ == '__main__':
    main()
