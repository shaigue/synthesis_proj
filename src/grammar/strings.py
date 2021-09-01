"""This file defines the grammar for strings, and formula translation from python expressions to Z3 formulas"""
from typing import Union, Set

from z3 import BoolRef, ArithRef, And, Or, Int, SeqRef, StringVal, String, SubString, Concat, Replace, PrefixOf, \
    SuffixOf, Contains, IndexOf, Length, Solver, sat

from adt.tree import Tree
from parsing.earley.grammar import Grammar
from src.generic_parser import GenericParser


class StringParser:
    def __init__(self, arith_variables: Set[str], string_variables: Set[str], min_num: int, max_num: int):
        grammar_str = _get_grammar_str(arith_variables, string_variables, min_num, max_num)
        tokens_str = _get_tokens_str(arith_variables.union(string_variables), min_num, max_num)
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


def _get_arith_var_str(variables: Set[str]) -> str:
    return "|".join(variables)


def _get_string_var_str(variables: Set[str]) -> str:
    return "|".join(variables)


def _get_var_str(variables: Set[str]) -> str:
    return _get_string_var_str(variables) + "|" + _get_arith_var_str(variables)


def _get_char_str() -> str:
    chr_to_str = lambda i: "\"" + chr(i) + "\""
    return "|".join(map(chr_to_str, range(ord('a'), ord('z') + 1))) + "|" + "|".join(map(chr_to_str, range(ord('A'), ord('Z') + 1)))


def _get_grammar_str(arith_variables: Set[str], string_variables: Set[str], min_num: int, max_num: int) -> str:
    """
    This function generates the strings grammar:
    1. LEXPR - Logical expression (expression with boolean value)
    2. SEXPR - String expression
    3. AEXPR - Arithmetic expression (expression with numeric value
    4. AFUNC - A function that returns an integer
    5. SLFUNC - A function that returns a boolean value
    6. SFUNC - A function that returns a string
    """
    numbers_str = _get_num_str(min_num, max_num)
    string_variables_str = _get_arith_var_str(string_variables)
    arith_variable_str = _get_string_var_str(arith_variables)
    # chars_str = _get_char_str()

    return "\n".join([
        "LEXPR -> ( AEXPR RELOP AEXPR ) | ( SEXPR RELOP SEXPR ) | ( LEXPR LOP LEXPR ) | SLFUNC",
        "SEXPR -> SVAR | SFUNC ",
        # "AEXPR -> AVAR | AEXPR AOP AEXPR | NUM | AFUNC ",
        "AEXPR -> AVAR | NUM | AFUNC ",
        "NUM -> " + numbers_str,
        "SVAR -> " + string_variables_str,
        "AVAR -> " + arith_variable_str,
        # "CHAR -> " + chars_str,
        "RELOP -> == | != | < | <=",
        "LOP -> and | or",
        "AOP -> + | - | * ",
        "AFUNC -> str_index_of ( SEXPR , SEXPR ) | str_len ( SEXPR )",
        "SLFUNC -> str_prefix_of ( SEXPR , SEXPR ) | str_suffix_of ( SEXPR , SEXPR ) |  str_contains ( SEXPR , SEXPR )",
        "SFUNC -> str_get_substring ( SEXPR , AEXPR , AEXPR ) | str_char_at_index ( SEXPR , AEXPR ) | str_concat ( SEXPR , SEXPR ) | str_replace ( SEXPR , SEXPR , SEXPR )"
    ])


def _get_tokens_str(variables: Set[str], min_num: int = 0, max_num: int = 5) -> str:
    string_functions = "str_get_substring|str_char_at_index|str_concat|str_replace"
    logical_functions = "str_prefix_of|str_suffix_of|str_contains"
    arithmetic_functions = "str_index_of|str_len"
    return (r"<=|<|!=|==|and|or|\)|\(|\+|-|\*|," + '|' + _get_var_str(variables) + '|' + _get_num_str(min_num, max_num) +
            "|" + string_functions + "|" + logical_functions + "|" + arithmetic_functions)


def _logic_expr_to_z3(tree: Tree) -> BoolRef:
    assert tree.root == "LEXPR"

    try:
        _, expr1, op_node, expr2, _ = tree.subtrees
    except ValueError:
        logical_func_node = tree.subtrees[0]
        return _logic_func_to_z3(logical_func_node)

    op = op_node.leaves[0].func

    if op_node.func == "RELOP" and expr1.func == "AEXPR":
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

    if op_node.func == "RELOP" and expr1.root == "SEXPR":
        expr1 = _str_expr_to_z3(expr1)
        expr2 = _str_expr_to_z3(expr2)
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


def _str_expr_to_z3(tree: Tree) -> SeqRef:
    assert tree.root == "SEXPR"

    if tree.subtrees[0].func == "SFUNC":
        return _str_func_to_z3(tree.subtrees[0])

    terminal = tree.leaves[0].func
    if "\"" in terminal:
        return StringVal(terminal.replace("\"", ""))
    else:
        return String(terminal)


def _logic_func_to_z3(tree: Tree) -> BoolRef:
    assert tree.root == "SLFUNC"

    func_name = tree.subtrees[0].func

    _, _, sexpr1, _, sexpr2, _ = tree.subtrees
    sexpr1 = _str_expr_to_z3(sexpr1)
    sexpr2 = _str_expr_to_z3(sexpr2)
    if func_name == "str_prefix_of":
        return PrefixOf(sexpr1, sexpr2)
    elif func_name == "str_suffix_of":
        return SuffixOf(sexpr1, sexpr2)
    elif func_name == "str_contains":
        return Contains(sexpr1, sexpr2)


def _str_func_to_z3(tree: Tree) -> SeqRef:
    assert tree.root == "SFUNC"

    func_name = tree.subtrees[0].func

    if func_name == "str_get_substring":
        _, _, sexpr1, _, aexpr1, _, aexpr2, _ = tree.subtrees
        sexpr1 = _str_expr_to_z3(sexpr1)
        aexpr1 = _arith_expr_to_z3(aexpr1)
        aexpr2 = _arith_expr_to_z3(aexpr2)
        return SubString(sexpr1, aexpr1, aexpr2)
    elif func_name == "str_char_at_index":
        _, _, sexpr1, _, aexpr1, _ = tree.subtrees
        sexpr1 = _str_expr_to_z3(sexpr1)
        aexpr1 = _arith_expr_to_z3(aexpr1)
        return SubString(sexpr1, aexpr1, 1)
    elif func_name == "str_concat":
        _, _, sexpr1, _, sexpr2, _ = tree.subtrees
        sexpr1 = _str_expr_to_z3(sexpr1)
        sexpr2 = _str_expr_to_z3(sexpr2)
        return Concat(sexpr1, sexpr2)
    elif func_name == "str_replace":
        _, _, sexpr1, _, sexpr2, _, sexpr3, _ = tree.subtrees
        sexpr1 = _str_expr_to_z3(sexpr1)
        sexpr2 = _str_expr_to_z3(sexpr2)
        sexpr3 = _str_expr_to_z3(sexpr3)
        return Replace(sexpr1, sexpr2, sexpr3)
    else:
        assert False


def _arith_func_to_z3(tree: Tree) -> ArithRef:
    assert tree.root == "AFUNC"

    func_name = tree.subtrees[0].func
    if func_name == "str_index_of":
        _, _, sexpr1, _, sexpr2, _ = tree.subtrees
        sexpr1 = _str_expr_to_z3(sexpr1)
        sexpr2 = _str_expr_to_z3(sexpr2)
        return IndexOf(sexpr1, sexpr2)
    elif func_name == "str_len":
        _, _, sexpr, _ = tree.subtrees
        sexpr = _str_expr_to_z3(sexpr)
        return Length(sexpr)


def _arith_expr_to_z3(tree: Tree) -> Union[ArithRef, int]:
    assert tree.root == "AEXPR"

    if len(tree.subtrees) == 1 and tree.subtrees[0].func != "AFUNC":
        terminal = tree.leaves[0].func
        if terminal.isnumeric():
            return int(terminal)
        else:
            return Int(terminal)

    elif tree.subtrees[0].func == "AFUNC":
        return _arith_func_to_z3(tree.subtrees[0])

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
    print(_get_tokens_str({'x', 'y'}, 0, 5))
    print(_get_grammar_str(set(), {'x', 'y'}, 0, 5))
    s_parser = StringParser(set(), {'x', 'y'}, 0, 5)
    print("---------------- 1 ----------------")
    exp1 = "(str_prefix_of(x,y) and str_contains(y, x))"
    z1 = s_parser.compile_to_z3(exp1)
    print(z1)
    s = Solver()
    s.add(z1)
    if s.check() == sat:
        print(s.model())
    else:
        print("Unsat")
    print("---------------- 2 ----------------")
    exp2 = "(((str_index_of(x, y) < 3) or str_contains(y, str_concat(x, y))) and (3 < str_len(y)))"
    z2 = s_parser.compile_to_z3(exp2)
    print(z2)
    s = Solver()
    s.add(z2)
    if s.check() == sat:
        print(s.model())
    else:
        print("Unsat")
    print("---------------- 3 ----------------")
    exp3 = "((str_index_of(x, y) == 4) and (str_len(x) == 2))"
    z3 = s_parser.compile_to_z3(exp3)
    print(z3)
    s = Solver()
    s.add(z3)
    if s.check() == sat:
        print(s.model())
    else:
        print("Unsat")
    print("---------------- 4 ----------------")
    exp4 = "((str_char_at_index(x, 5) == y) and (str_get_substring(x, 0, 2) == y))"
    z4 = s_parser.compile_to_z3(exp4)
    print(z4)
    s = Solver()
    s.add(z4)
    if s.check() == sat:
        print(s.model())
    else:
        print("Unsat")


if __name__ == '__main__':
    main()
