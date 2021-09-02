from typing import Callable, List, Dict, Any, Type

from z3 import And, BoolRef, Solver, Not, sat, Implies, Int

from src.enumeration_new import bottom_up_enumeration_with_observational_equivalence


# TODO: give timeout parameters in case the synthesizer does not find any solution
# TODO: maybe for every different set of input (strings, integers, arrays) assign a function, constants
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


def counter_example_synthesis(positive_examples: List[Dict[str, Any]], functions: List[Callable], constants: List,
                              property_to_prove: BoolRef, max_counter_examples=10):
    var_name_to_type = {name: type(value) for name, value in positive_examples[0].items()}
    negative_examples = []

    for counter_example_i in range(max_counter_examples):
        assumption = find_satisfying_expr(positive_examples, negative_examples, functions, constants)
        counter_example = _find_counter_example(assumption, property_to_prove, var_name_to_type)
        if counter_example is None:
            return assumption
        else:
            negative_examples.append(counter_example)


def _find_counter_example(a: BoolRef, b: BoolRef, var_name_to_type: Dict[str, Type]):
    s = Solver()
    s.add(Not(Implies(a, b)))
    res = s.check()

    if res == sat:
        counter_example = {}
        for var_name, t in var_name_to_type.items():
            # TODO: add support to arrays
            if t == int:
                counter_example[var_name] = 0
            elif t == str:
                counter_example[var_name] = ""
            else:
                assert False, f"Does not support {t}"

        model = s.model()
        for model_var in model:
            var_name = str(model_var)
            if var_name in var_name_to_type:
                # TODO: add support to arrays
                t = var_name_to_type[var_name]
                value = model[model_var]
                if t == int:
                    value = value.as_long()
                elif t == str:
                    value = value.as_string()
                else:
                    assert False, f"Does not support {t}"

                counter_example[var_name] = value

        return counter_example


def main():
    from src.library.integers import add, sub, eq, lt, mul
    positive_examples = [{'x': 10, 'y': 1}, {'x': 20, 'y': 13}, {'x': 12, 'y': 2}]
    # negative_examples = [{'x': 1, 'y': -2}, {'x': -1, 'y': -2}, {'x': -1, 'y': 3}]
    safety_property = And(Int('x') > 2, Int('y') > 0, Int('x') > Int('y'))
    functions = [add, sub, eq, lt, mul]
    constants = [0, 1]
    expr = counter_example_synthesis(positive_examples, functions, constants, safety_property)
    print(expr)


if __name__ == '__main__':
    main()
