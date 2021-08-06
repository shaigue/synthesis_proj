# bottom-up enumeration of a grammer with observational equivalence
from typing import List

from parsing.earley.parse_trees import ParseTrees
from parsing.earley.parser import Parser, Grammar
from parsing.silly import SillyLexer

MAX_DEPTH = 2


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


def replace_non_terminals(rule_rhs: List[str], final_expressions, result=None) -> List[str]:
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
        if " ".join(rule_rhs) not in result:
            result.append(" ".join(rule_rhs))
        return result

    # Go over all possible expressions for this non terminal
    for expr in final_expressions[non_terminal]:
        new_rhs = rule_rhs[:]
        new_rhs[i] = expr
        # For each expression - replace the non terminal with this expression, and make a recursive call
        result = replace_non_terminals(new_rhs, final_expressions, result)

    return result


def enumerate_programs(grammar_str, tokens_str):
    """
    :param grammar_str: string describing grammar
    :param tokens_str: string describing tokens as regexp (or list of such strings)
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
            for rule in grammar.rules[lhs]:
                # For each rule, use previous results to create new expressions
                if not is_final(" ".join(rule.rhs)):
                    try:
                        result = replace_non_terminals(rule.rhs, programs)
                        for item in result:
                            yield item

                        programs[lhs] = programs.setdefault(lhs, []) + result
                    except KeyError:
                        pass


if __name__ == "__main__":
    tokens = r"a|b|c|<=|<|!=|==|and|or|\)|\("
    grammar_string = r"""
    LEXPR -> ( VAR RELOP VAR ) | ( LEXPR LOP LEXPR )
    VAR -> a | b | c
    RELOP -> == | != | < | <=
    LOP -> and | or
    """
    enumerator = enumerate_programs(grammar_string, tokens)
    for j in range(100):
        print(next(enumerator))

