# bottom-up enumeration of a grammar with observational equivalence
from typing import List
from datetime import datetime

from parsing.earley.parse_trees import ParseTrees
from parsing.earley.parser import Parser, Grammar
from parsing.silly import SillyLexer

MAX_DEPTH = 4


class GenericParser(object):
    def __init__(self, tokens: str, grammar: str):
        """
        return a parser of a given language grammar
        :param tokens: A string describing the tokens (regexp)
        :param grammar: string describing grammar
            example format:
            LEXPR -> ( VAR RELOP VAR ) | LEXPR LOP LEXPR
            VAR -> a | b | x | y | z
            RELOP -> == | != | < | <=
            LOP -> and | or
        """
        self.tokenizer = SillyLexer(tokens)
        self.grammar = Grammar.from_string(grammar)

    def __call__(self, program_text):
        tokens = list(self.tokenizer(program_text))

        earley = Parser(grammar=self.grammar, sentence=tokens, debug=False)
        earley.parse()

        if earley.is_valid_sentence():
            trees = ParseTrees(earley)
            assert (len(trees) == 1)
            return trees
        else:
            return None


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
    :return: a tuple of boolean values of the same length as the inputs list
    """
    ret = tuple()

    for inp in inputs:
        try:
            val = eval(program, {}, inp)
#            if isinstance(val, bool):
            ret += (eval(program, {}, inp),)
        except SyntaxError:
            # received an incomplete program, nothing ot eval
            pass
        except ZeroDivisionError:
            ret += (None,)

    return ret


def replace_non_terminals(rule_lhs: str, rule_rhs: List[str], final_expressions, inputs, result=None) -> List[str]:
    result = [] if result is None else result

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
        start_t = datetime.now()
        existing_eq_classes = [evaluate_program(prog, inputs) for prog in result] + [evaluate_program(prog, inputs) for prog in final_expressions[rule_lhs]]
        print(datetime.now() - start_t)
        values = evaluate_program(expr, inputs)
        if values not in existing_eq_classes or values == ():
            result.append(expr)
            # print(expr)
        return result

    # Go over all possible expressions for this non terminal

    for expr in final_expressions[non_terminal]:
        new_rhs = rule_rhs[:]
        new_rhs[i] = expr
        # if i == 0:
            # print(new_rhs)
            # print(datetime.now())
        # For each expression - replace the non terminal with this expression, and make a recursive call
        result = replace_non_terminals(rule_lhs, new_rhs, final_expressions, inputs, result)

    return result


def enumerate_programs(grammar_str, inputs, base_rule):
    """
    :param grammar_str: string describing grammar
    :param inputs: list of dicts, each dict contains var names and their values
    :return: yields programs under this grammar
    """
    grammar = Grammar.from_string(grammar_str)

    # 'programs' is a dictionary - keys are LHS of grammar rules,
    # values are expressions that match the LHS
    programs = {lhs: [] for lhs in grammar.rules.keys()}
    for lhs in programs.keys():
        # Create depth-0 - all final expressions of depth 0
        for rule in grammar.rules[lhs]:
            if is_final(" ".join(rule.rhs)):
                programs[lhs].append(" ".join(rule.rhs))

    for i in range(1, MAX_DEPTH):
        for lhs in grammar.rules:
            result = []
            for rule in grammar.rules[lhs]:
                # For each rule, use previous results to create new expressions
                if not is_final(" ".join(rule.rhs)):
                    try:
                        result += programs.setdefault(lhs, []) + replace_non_terminals(lhs, rule.rhs, programs, inputs)
                    except KeyError:
                        pass
            programs[lhs] = programs.setdefault(lhs, []) + result
        print("finished depth")
        print(datetime.now())
        for program in programs[base_rule]:
            yield program


if __name__ == "__main__":
    tokens = r"a|b|c|<=|<|!=|==|and|or|\)|\("
    grammar_string = r"""
    LEXPR -> ( AEXPR RELOP AEXPR ) | ( LEXPR LOP LEXPR )
    AEXPR -> VAR | AEXPR AOP AEXPR | NUM
    NUM -> 1 | 2 | 3 | 4 | 5 | 0
    VAR -> x | y | z
    RELOP -> == | != | < | <=
    LOP -> and | or
    AOP -> + | - | * | / | %
    """
    inputs_dict = [
        {
            "x": 0,
            "y": 0,
            "z": 0,
            "temp": 0
        },
        {
            "x": 1,
            "y": 2,
            "z": -1,
            "temp": -1
        },
        {
            "x": 2,
            "y": 1,
            "z": 1,
            "temp": 1
        },
        {
            "x": 3,
            "y": 3,
            "z": 0,
            "temp": 0
        },
        {
            "x": 4,
            "y": 2,
            "z": 2,
            "temp": 2
        },
        {
            "x": 5,
            "y": 4,
            "z": 1,
            "temp": 1
        },
        {
            "x": 6,
            "y": 3,
            "z": 3,
            "temp": 3
        },
        {
            "x": 7,
            "y": 5,
            "z": 2,
            "temp": 2
        },
        {
            "x": 8,
            "y": 4,
            "z": 4,
            "temp": 4
        },
        {
            "x": 9,
            "y": 6,
            "z": 3,
            "temp": 3
        }
    ]
    print(datetime.now())
    enumerator = enumerate_programs(grammar_string, inputs_dict, "LEXPR")
    for prog in enumerator:
        print(prog)

