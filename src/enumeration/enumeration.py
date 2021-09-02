"""
In this work we assume a very simple grammar, similar to FOL.
The grammar contains functions, variables, and constants.
Hight 0 contains the constants and the variables, and functions are applied to increase the depth.
"""
# TODO: currently, expressions are strings, might use a special object later
# TODO: use the conjunction heuristic

import inspect
import itertools
from collections import defaultdict
from typing import List, Callable, Any, Dict, Tuple, Type


class Language:
    def __init__(self, functions: List[Callable], variables: List[str], constants: List[Any]):
        self.functions = functions
        self.variables = variables
        self.constants = constants

    def bottom_up_enumeration_with_observational_equivalence(self, examples: List[Dict[str, Any]]):
        typed_value_vector_to_expr = self._init_value_vector_to_expr(examples)

        while True:
            new_typed_value_vector_to_expr = defaultdict(dict)

            for func in self.functions:
                for value_vector_list, expr_list in self._iter_params(func, typed_value_vector_to_expr):
                    value_vector = tuple(func(*params) for params in zip(*value_vector_list))
                    t = type(value_vector[0])

                    if value_vector not in typed_value_vector_to_expr[t] and \
                            value_vector not in new_typed_value_vector_to_expr[t]:

                        expr = f"{func.__name__}({', '.join(expr_list)})"
                        new_typed_value_vector_to_expr[t][value_vector] = expr
                        yield value_vector, expr

            if len(new_typed_value_vector_to_expr) == 0:
                return

            for t, new_value_vector_to_expr in new_typed_value_vector_to_expr.items():
                if t in typed_value_vector_to_expr:
                    typed_value_vector_to_expr[t].update(new_value_vector_to_expr)
                else:
                    typed_value_vector_to_expr[t] = new_value_vector_to_expr

    @staticmethod
    def _iter_params(func: Callable, typed_value_vector_to_expr: Dict[Type, Dict[Tuple, str]]):
        """Assumes that the functions are annotated with types"""
        func_sig = inspect.signature(func)
        product_sets = []
        for param in func_sig.parameters.values():
            t = param.annotation
            product_sets.append(typed_value_vector_to_expr[t].items())

        for value_vector_expr_pair_list in itertools.product(*product_sets):
            value_vector_list = []
            expr_list = []

            for value_vector, expr in value_vector_expr_pair_list:
                value_vector_list.append(value_vector)
                expr_list.append(expr)

            yield value_vector_list, expr_list

    def _init_value_vector_to_expr(self, examples: List[Dict[str, Any]]):
        typed_value_vector_to_expr = defaultdict(dict)

        for constant in self.constants:
            value_vector = (constant,) * len(examples)
            t = type(value_vector[0])
            if value_vector not in typed_value_vector_to_expr[t]:
                typed_value_vector_to_expr[t][value_vector] = str(constant)

        for variable in self.variables:
            value_vector = tuple(example[variable] for example in examples)
            t = type(value_vector[0])
            if value_vector not in typed_value_vector_to_expr[t]:
                typed_value_vector_to_expr[t][value_vector] = variable

        return typed_value_vector_to_expr


def main():
    from src.library.integer_functions import add, sub, eq
    language = Language(
        functions=[add, sub, eq],
        variables=['x', 'y'],
        constants=[0, 1]
    )
    examples = [{'x': 0, 'y': 0}, {'x': 1, 'y': -1}]
    for i, (value_vector, expr) in enumerate(language.bottom_up_enumeration_with_observational_equivalence(examples)):
        print(i)
        print(expr)
        print(value_vector)
        if i == 100:
            break


if __name__ == '__main__':
    main()
