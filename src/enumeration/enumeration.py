"""
In this work we assume a very simple grammar, similar to FOL.
The grammar contains functions, variables, and constants.
Hight 0 contains the constants and the variables, and functions are applied to increase the depth.
"""


class Language:
    def __init__(self, functions: List[Callable], variables: List[str], constants: List[Any]):
        self.functions = functions
        self.variables = variables
        self.constants = constants


def bottom_up_enumeration_with_observational_equivalence(language: Language, examples: List[Dict[str, Any]]):
    # TODO: implement
    pass
