from typing import Callable, List, Dict, Any, Type
import z3

from z3 import And, BoolRef, Solver, Not, sat, Implies, Int, FuncInterp, ModelRef, unsat

from src.enumeration import bottom_up_enumeration_with_observational_equivalence
from config import ARRAY_LEN
z3.set_param('model.compact', False)


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
                              property_to_prove: BoolRef, max_counter_examples=20):
    # TODO: what if one of the positive examples does not satisfy the the property to prove?
    #  if so, we can be certain that we don't have any loop invariant. add this check

    var_name_to_type = {name: type(value) for name, value in positive_examples[0].items()}
    negative_examples = []

    for counter_example_i in range(max_counter_examples):
        assumption = find_satisfying_expr(positive_examples, negative_examples, functions, constants)
        counter_example = _find_counter_example(assumption, property_to_prove, var_name_to_type)
        if counter_example.counter_example_found:
            negative_examples.append(counter_example.example)
        else:
            return assumption


def _z3_array_to_list(arr, model):
    if isinstance(arr, FuncInterp):
        f = _z3_to_fun(arr)
        ret_val = [f(i) for i in range(ARRAY_LEN)]
        return ret_val

    ret_val = [arr[i] for i in range(ARRAY_LEN)]
    ret_val = [model.evaluate(entry) for entry in ret_val]
    ret_val = [entry.as_long() for entry in ret_val]
    return ret_val


def _has_func_interp(model: ModelRef) -> bool:
    for variable in model:
        value = model[variable]
        if isinstance(value, FuncInterp):
            return True

    return False


class _CounterExampleResult:
    def __init__(self, counter_example_found: bool, example: Dict[str, Any] = None):
        self.counter_example_found = counter_example_found
        self.example = example

    @classmethod
    def no_counter_example(cls):
        return cls(counter_example_found=False)

    @classmethod
    def counter_example(cls, example: Dict[str, Any]):
        return cls(counter_example_found=True, example=example)


class _FuncInterpException(Exception):
    pass


def _z3_to_fun(z3_expr: FuncInterp):
    """Takes a FuncInterp instance, and returns the function which
    takes as input a z3 expression and returns the value of the
    corresponding expression.

    Mutually recursive with z3_to_val

    Arguments:
    - `z3_expr`: an instance of FuncInterp
    """
    fun_list = z3_expr.as_list()
    other_val = _z3_to_val(fun_list.pop())
    fun_list_val = [(str(_z3_to_val(p[0])), _z3_to_val(p[1]))
                    for p in fun_list]
    fun_dict = dict(fun_list_val)

    def fun(a):
        try:
            return fun_dict[str(a)]
        except KeyError:
            return other_val

    return fun


def _z3_to_val(z3_expr):
    """Send a z3 expression to its value
    as a python expression, if it has one,
    otherwise return the expresson itself.

    Arguments:
    - `z3_expr`: a z3 AST
    """
    if z3.is_int_value(z3_expr):
        return z3_expr.as_long()
    elif z3.is_true(z3_expr):
        return True
    elif z3.is_false(z3_expr):
        return False
    elif isinstance(z3_expr, z3.FuncInterp):
        return _z3_to_fun(z3_expr)
    else:
        return z3_expr


def _find_counter_example(a: BoolRef, b: BoolRef, var_name_to_type: Dict[str, Type]) -> _CounterExampleResult:
    s = Solver()
    s.add(Not(Implies(a, b)))
    res = s.check()

    if res == unsat:
        return _CounterExampleResult.no_counter_example()

    counter_example = {}
    for var_name, t in var_name_to_type.items():
        if t == int:
            counter_example[var_name] = 0
        elif t == str:
            counter_example[var_name] = ""
        elif t == list:
            counter_example[var_name] = [0] * ARRAY_LEN
        else:
            assert False, f"Does not support {t}"

    model = s.model()
    # TODO: quick fix, but there should be a way better handle FuncInterp
    # if _has_func_interp(model):
    #     raise _FuncInterpException

    for model_var in model:
        var_name = str(model_var)
        if var_name in var_name_to_type:
            t = var_name_to_type[var_name]
            value = model[model_var]

            if t == int:
                value = value.as_long()
            elif t == str:
                value = value.as_string()
            elif t == list:
                value = _z3_array_to_list(value, model)
            else:
                assert False, f"Does not support {t}"

            counter_example[var_name] = value

    return _CounterExampleResult.counter_example(example=counter_example)


def main():
    from src.library import get_int_functions_and_constants
    positive_examples = [{'x': 10, 'y': 1}, {'x': 20, 'y': 13}, {'x': 12, 'y': 2}]
    # negative_examples = [{'x': 1, 'y': -2}, {'x': -1, 'y': -2}, {'x': -1, 'y': 3}]
    safety_property = And(Int('x') > 2, Int('y') > 0, Int('x') > Int('y'))
    functions, constants = get_int_functions_and_constants()
    expr = counter_example_synthesis(positive_examples, functions, constants, safety_property)
    print(expr)


if __name__ == '__main__':
    main()
