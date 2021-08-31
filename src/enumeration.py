from typing import List, Dict
from parsing.earley.parser import Grammar
from datetime import datetime
from itertools import combinations
import config
from inspect import getmembers, isfunction

from pathlib import Path
from src.test_utils.positive_state_extractor import collect_positive_states_from_file
import grammar.str_utils

MAX_DEPTH = 4


def evaluate_predicate(predicate: str, inputs: List[Dict]):
    ret = tuple()
    # TODO - can throw a NameError when one of the variables in the predicate are not defined in the state.
    #   should be an invalid predicate
    for inp in inputs:
        try:
            functions = {name: func for name, func in getmembers(grammar.str_utils, isfunction)}
            ret += (eval(predicate, functions, inp),)
        except SyntaxError:
            # received an incomplete predicate, nothing ot eval
            return (predicate,)
        except (ZeroDivisionError, IndexError):
            ret += (None,)

    return ret


def is_final(predicate: List[str]) -> bool:
    for word in predicate:
        if word.isupper():
            return False
    return True


def predicates_from_rule_generator(rule: List[str], predicates, depth):
    if is_final(rule):
        yield ' '.join(rule)

    non_terminal_index = 0
    non_terminal = ""
    for i, word in enumerate(rule):
        if word.isupper():
            non_terminal_index = i
            non_terminal = word
            break

    # Find the deepest depth in which we have programs to replace the non terminal
    lookup_depth = depth - 1
    for d in range(lookup_depth, -1, -1):
        if non_terminal in predicates[d] and predicates[d][non_terminal]:
            lookup_depth = d
            break

    for evaluation, replacement in predicates[1].get(non_terminal, {}).items():
        new_rule = rule[:non_terminal_index] + replacement.split(" ") + rule[non_terminal_index + 1:]
        yield from predicates_from_rule_generator(new_rule, predicates, depth)

    for evaluation, replacement in predicates[lookup_depth].get(non_terminal, {}).items():
        new_rule = rule[:non_terminal_index] + replacement.split(" ") + rule[non_terminal_index + 1:]
        yield from predicates_from_rule_generator(new_rule, predicates, depth)


def enumerate_predicates(grammar: Grammar, positive_inputs: List[Dict], negative_inputs: List[Dict]):
    """
    enumerate over given grammar, with observational equivalence (Generator)
    programs are kept in the predictes dictionary, of type Dict[int, Dict[str, Dict[tuple, str]]]
    key of uppermost dict is depth, key of next dict is lhs of the rule, key of next dict is tuple of results from
    the evaluation of the predicate on different input (length of tuple is amount of inputs).
    :param grammar: the grammar
    :param positive_inputs: inputs on which the LI should be evaluated to True
    :param negative_inputs: inputs on which the LI should be evaluated to False
    :return: yields programs, from depth 0 until MAX_DEPTH
    """
    inputs = positive_inputs + negative_inputs
    # Deal with depth = 0
    predicates = {0: {}}
    for lhs, rhs_list in grammar.rules.items():
        predicates[0][lhs] = {}
        for rhs in rhs_list:
            pred = ' '.join(rhs.rhs)
            if is_final(rhs.rhs):
                evaluation = evaluate_predicate(pred, inputs)
                if evaluation not in predicates[0][lhs]:
                    predicates[0][lhs][evaluation] = pred
                    if lhs == grammar.start_symbol:
                        yield pred

    for i in range(1, MAX_DEPTH + 1):
        predicates[i] = {}
        for lhs, rhs_list in grammar.rules.items():
            predicates[i][lhs] = {}
            for rhs in rhs_list:
                for new_predicate in predicates_from_rule_generator(rhs.rhs, predicates, i):
                    evaluation = evaluate_predicate(new_predicate, inputs)
                    if all([evaluation not in predicates[k][lhs] for k in range(i+1)]):
                        predicates[i][lhs][evaluation] = new_predicate

        for predicate in predicates[i][grammar.start_symbol].values():
            yield predicate

        positive_predicates = [pred for evaluation, pred in predicates[i][grammar.start_symbol].items()
                               if len(list(filter(lambda x: not x, evaluation[:len(positive_inputs)]))) == 0]

        for d in range(2, 4):
            positive_groups = list(combinations(positive_predicates, d))
            for g in positive_groups:
                ret = (d - 1) * "( " + f"{g[0]}"
                for p in g[1:]:
                    ret += f" and {p} )"
                yield ret


def find_loop_invariant(grammar: Grammar, positive_inputs: List[Dict], negative_inputs: List[Dict]) -> str:
    for pred in enumerate_predicates(grammar, positive_inputs, negative_inputs):
        positive_states_results = evaluate_predicate(pred, positive_inputs)
        negative_states_results = evaluate_predicate(pred, negative_inputs)

        if not None in positive_states_results and not None in negative_states_results:
            if all(positive_states_results) and not any(negative_states_results):
                return pred


if __name__ == "__main__":
    grammar_str = "\n".join([
        "LEXPR -> ( AEXPR RELOP AEXPR ) | ( SEXPR RELOP SEXPR ) | ( LEXPR LOP LEXPR ) | SLFUNC",
        "SEXPR -> SVAR | SFUNC ",
        "AEXPR -> AVAR | AEXPR AOP AEXPR | NUM | AFUNC ",
        "NUM -> 0|1|2|3|4|5",
        "SVAR -> s1|s2",
        "AVAR -> i",
        # "CHAR -> " + chars_str,
        "RELOP -> == | != | < | <=",
        "LOP -> and | or",
        "AOP -> + | - | * ",
        "AFUNC -> str_index_of ( SEXPR , SEXPR ) | str_len ( SEXPR )",
        "SLFUNC -> str_prefix_of ( SEXPR , SEXPR ) | str_suffix_of ( SEXPR , SEXPR ) |  str_contains ( SEXPR , SEXPR )",
        "SFUNC -> str_get_substring ( SEXPR , AEXPR , AEXPR ) | str_char_at_index ( SEXPR , AEXPR ) | str_concat ( SEXPR , SEXPR ) | str_replace ( SEXPR , SEXPR , SEXPR )"
    ])
    grammar_obj = Grammar.from_string(grammar_str)
    positive = [
        {
            "s1": "First string",
            "s2": "Second string",
            "i": 0
        },
        {
            "s1": "First string",
            "s2": "Second stringF",
            "i": 1
        },
        {
            "s1": "First string",
            "s2": "Second stringFi",
            "i": 2
        },
        {
            "s1": "First string",
            "s2": "Second stringFir",
            "i": 3
        },
        {
            "s1": "First string",
            "s2": "Second stringFirs",
            "i": 4
        },
        {
            "s1": "First string",
            "s2": "Second stringFirst",
            "i": 5
        },
        {
            "s1": "First string",
            "s2": "Second stringFirst ",
            "i": 6
        },
        {
            "s1": "First string",
            "s2": "Second stringFirst s",
            "i": 7
        },
        {
            "s1": "First string",
            "s2": "Second stringFirst st",
            "i": 8
        },
    ]
    negative = [
        {
            "s1": "ab",
            "s2": "",
            "i": 2
        }
    ]
    for le in find_loop_invariant(grammar_obj, positive, negative):
        print(le)
