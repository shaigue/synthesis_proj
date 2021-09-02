from typing import Callable, List, Dict, Any

from z3 import And

from src.enumeration.enumeration import bottom_up_enumeration_with_observational_equivalence


# TODO: maybe for every different set of input (strings, integers, arrays assign a function, constants
def find_satisfying_expr(positive_examples: List[Dict[str, Any]], negative_examples: List[Dict[str, Any]],
                         functions: List[Callable], constants: List):
    examples = positive_examples + negative_examples
    n_positive = len(positive_examples)
    n_negative = len(negative_examples)

    expr_negative_cover_pairs = []
    negative_examples_to_cover = set(range(n_negative))

    for value_vector, expr in bottom_up_enumeration_with_observational_equivalence(examples, functions, constants):
        if isinstance(value_vector[0], bool) and all(value_vector[i] for i in range(n_positive)):
            negative_cover = {i for i in range(n_negative) if not value_vector[n_positive + i]}
            other_negative_covers = (negative_cover0 for _, negative_cover0 in expr_negative_cover_pairs)

            if any(negative_cover.issubset(other_negative_cover) for other_negative_cover in other_negative_covers):
                continue

            expr_negative_cover_pairs = list(filter(lambda x: not x[1].issubset(negative_cover),
                                                    expr_negative_cover_pairs))
            expr_negative_cover_pairs.append((expr, negative_cover))
            negative_examples_to_cover.difference_update(negative_cover)

            if len(negative_examples_to_cover) == 0:
                if len(expr_negative_cover_pairs) > 1:
                    return And([expr for expr, _ in expr_negative_cover_pairs])
                return expr


def main():
    from src.library.integer_functions import add, sub, eq, lt, mul
    positive_examples = [{'x': 10, 'y': 1}, {'x': 2, 'y': 13}, {'x': 2, 'y': 2}]
    negative_examples = [{'x': 1, 'y': -2}, {'x': -1, 'y': -2}, {'x': -1, 'y': 3}]
    functions = [add, sub, eq, lt, mul]
    constants = [0, 1]
    expr = find_satisfying_expr(positive_examples, negative_examples, functions, constants)
    print(expr)


if __name__ == '__main__':
    main()
