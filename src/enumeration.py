# bottom-up enumeration of a grammar with observational equivalence
from typing import List, Dict, Tuple
from datetime import datetime

from parsing.earley.parser import Grammar

MAX_DEPTH = 5


def is_final(program):
    for c in program:
        if c.isupper():
            return False

    return True


def evaluate_program(program, inputs):
    """
    evalutaes a program against all given inputs (list of dicts)
    :param program: string representing the program (predicate)
    :param inputs: list of dicts, each dict contains a var name and its value
    :return: a tuple representing equivalence
    """
    ret = tuple()

    for inp in inputs:
        try:
            val = eval(program, {}, inp)
#            if isinstance(val, bool):
            ret += (eval(program, {}, inp),)
        except SyntaxError:
            # received an incomplete program, nothing ot eval
            return (program,)
        except ZeroDivisionError:
            ret += (None,)

    return ret


def replace_non_terminals(rule_lhs: str, rule_rhs: List[str], final_expressions: Dict[str, Dict[Tuple, str]], inputs, result=None) -> Dict[Tuple, str]:
    result = {} if result is None else result

    # Find the first non terminal
    i = 0
    non_terminal = None
    for index, item in enumerate(rule_rhs):
        if item.isupper():
            i = index
            non_terminal = item
            break

    # No non-terminal - This is a final program.
    if non_terminal is None:
        expr = " ".join(rule_rhs)
        # start_t = datetime.now()
        # existing_eq_classes = [evaluate_program(prog, inputs) for prog in result] + [evaluate_program(prog, inputs) for prog in final_expressions[rule_lhs]]
        # print(datetime.now() - start_t)
        values = evaluate_program(expr, inputs)
        if values not in result.keys() and values not in final_expressions[rule_lhs].keys():
            result[values] = expr
            # print(expr)
        return result

    # Go over all possible expressions for this non terminal

    for expr in final_expressions[non_terminal].values():
        new_rhs = rule_rhs[:]
        new_rhs[i] = expr
        # For each expression - replace the non terminal with this expression, and make a recursive call
        result = replace_non_terminals(rule_lhs, new_rhs, final_expressions, inputs, result)

    return result


def merge_dicts(dst: Dict[Tuple, str], src: Dict[Tuple, str]):
    for k, v in src.items():
        if k not in dst.keys():
            dst[k] = v


def enumerate_programs(grammar_str, inputs, base_rule):
    """
    :param grammar_str: string describing grammar
    :param inputs: list of dicts, each dict contains var names and their values
    :return: yields programs under this grammar
    """
    grammar = Grammar.from_string(grammar_str)

    # 'programs' is a dictionary - keys are LHS of grammar rules,
    # values are expressions that match the LHS
    programs = {lhs: {} for lhs in grammar.rules.keys()}
    for lhs in programs.keys():
        # Create depth-0 - all final expressions of depth 0
        for rule in grammar.rules[lhs]:
            expr = " ".join(rule.rhs)
            if is_final(expr):
                programs[lhs][evaluate_program(expr, inputs)] = expr

    for i in range(1, MAX_DEPTH):
        for lhs in grammar.rules:
            result = {}
            for rule in grammar.rules[lhs]:
                # For each rule, use previous results to create new expressions
                if not is_final(" ".join(rule.rhs)):
                    try:
                        merge_dicts(result, replace_non_terminals(lhs, rule.rhs, programs, inputs))
                    except KeyError:
                        pass
            merge_dicts(programs[lhs], result)
        print("finished depth")
        print(datetime.now())
        for prog in programs[base_rule].values():
            yield prog


if __name__ == "__main__":
    tokens = r"a|b|c|<=|<|!=|==|and|or|\)|\("
    grammar_string = r"""
    LEXPR -> ( AEXPR RELOP AEXPR ) | ( LEXPR LOP LEXPR )
    AEXPR -> VAR | AEXPR AOP AEXPR | NUM
    NUM -> 1 | 2 | 3 | 4 | 5 | 0
    VAR -> x | y | z
    RELOP -> == | != | < | <=
    LOP -> and | or
    AOP -> + | - | * | // | %
    """
    inputs_dict = [
        {
            "x": 1,
            "y": 2,
            "z": 3
        },
        {
            "x": 2,
            "y": 3,
            "z": 3
        }
    ]
    print(datetime.now())
    enumerator = enumerate_programs(grammar_string, inputs_dict, "LEXPR")
    for prog in enumerator:
        print(prog)

