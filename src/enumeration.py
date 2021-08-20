from typing import List, Dict
from parsing.earley.parser import Grammar
from datetime import datetime
import config

from pathlib import Path
from test_utils.positive_state_extractor import collect_positive_states_from_file

MAX_DEPTH = 4


def evaluate_predicate(predicate: str, inputs: List[Dict]):
    ret = tuple()

    for inp in inputs:
        try:
            val = eval(predicate, {}, inp)
            # if isinstance(val, bool):
            ret += (eval(predicate, {}, inp),)
        except SyntaxError:
            # received an incomplete predicate, nothing ot eval
            return (predicate,)
        except ZeroDivisionError:
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

    for evaluation, replacement in predicates[lookup_depth].get(non_terminal, {}).items():
        new_rule = rule[:non_terminal_index] + replacement.split(" ") + rule[non_terminal_index + 1:]
        yield from predicates_from_rule_generator(new_rule, predicates, depth)


def enumerate_predicates(grammar: Grammar, inputs: List[Dict]):
    """
    enumerate over given grammar, with observational equivalence (Generator)
    programs are kept in the predictes dictionary, of type Dict[int, Dict[str, Dict[tuple, str]]]
    key of uppermost dict is depth, key of next dict is lhs of the rule, key of next dict is tuple of results from
    the evaluation of the predicate on different input (length of tuple is amount of inputs).
    :param grammar: the grammar
    :param inputs: inputs on which to base the observational equivalence
    :return: yields programs, from depth 0 until MAX_DEPTH
    """
    # Deal with depth = 0
    predicates = {0: {}}
    for lhs, rhs_list in grammar.rules.items():
        for rhs in rhs_list:
            pred = ' '.join(rhs.rhs)
            if is_final(rhs.rhs):
                evaluation = evaluate_predicate(pred, inputs)
                if evaluation not in predicates[0].setdefault(lhs, {}):
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
                    predicates[i][lhs][evaluation] = new_predicate

        for predicate in predicates[i][grammar.start_symbol].values():
            yield predicate


def find_loop_invariant(grammar_string: str, positive_inputs: [List[Dict]], negative_inputs: List[Dict]) -> str:
    grammar = Grammar.from_string(grammar_string)
    for pred in enumerate_predicates(grammar, positive_inputs + negative_inputs):
        print(pred)
        if (len(list(filter(lambda x: not x, evaluate_predicate(pred, positive_inputs)))) == 0 and
                len(list(filter(lambda x: x, evaluate_predicate(pred, negative_inputs)))) == 0):
            return pred


if __name__ == "__main__":
    tokens = r"x|y|z|<=|<|!=|==|and|or|\)|\(|\+|-|\*|/|%"
    grammar_string = r"""
    LEXPR -> ( AEXPR RELOP AEXPR ) | ( LEXPR LOP LEXPR )
    AEXPR -> VAR | AEXPR AOP AEXPR | NUM
    NUM -> 1 | 2 | 3 | 4 | 5 | 0
    VAR -> x | y | z | temp
    RELOP -> == | != | < | <=
    LOP -> and | or
    AOP -> + | - | * | // | %
    """

    file = config.TESTS_DIR / 'integer_tests' / '3' / 'program.py'
    positive = collect_positive_states_from_file(file)
    positive[0]['temp'] = -1
    negative = [
        {
            "x": 6,
            "temp": -21,
            "z": 7,
            "y": 86
        },
        {
            "x": -87,
            "temp": -31,
            "z": 32,
            "y": 1
        },
        {
            "x": 89,
            "temp": -93,
            "z": -28,
            "y": -75
        },
        {
            "x": 76,
            "temp": -15,
            "z": -73,
            "y": 64
        },
        {
            "x": -52,
            "temp": -96,
            "z": 80,
            "y": 12
        }
    ]
    start = datetime.now()
    print(start)
    print(find_loop_invariant(grammar_string, positive, negative))
    print(datetime.now() - start)
