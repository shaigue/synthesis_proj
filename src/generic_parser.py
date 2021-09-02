# TODO: if not needed anymore delete this file
from parsing.earley.parse_trees import ParseTrees
from parsing.earley.parser import Parser, Grammar
from parsing.silly import SillyLexer


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


if __name__ == "__main__":
    tokens = r"x|y|z|<=|<|!=|==|and|or|\)|\(|\+|-|\*|/|%"
    grammar_string = r"""
    LEXPR -> ( AEXPR RELOP AEXPR ) | ( LEXPR LOP LEXPR )
    AEXPR -> VAR | AEXPR AOP AEXPR | NUM
    NUM -> 1 | 2 | 3 | 4 | 5 | 0
    VAR -> x | y | z
    RELOP -> == | != | < | <=
    LOP -> and | or
    AOP -> + | - | * | // | %
    """
    prog = "( ( x < y ) or ( z < x ) )"
    t = GenericParser(tokens, grammar_string)(prog)
    print(t)
