from typing import Callable, List, Dict, Any, Type, Union, Tuple, Optional
import z3

from z3 import And, BoolRef, Solver, Not, sat, Implies, Int, FuncInterp, ModelRef, unsat, unknown, Lambda, If, Length

import config
from src.int_seq_utils import IntSeq
from src.enumeration import bottom_up_enumeration_with_observational_equivalence, var_to_z3
from config import ARRAY_LEN
z3.set_param('model.compact', False)


# TODO: add timeout based on time, and not on the number of counter examples
# TODO: try to minimize when doing conjuction of the formulas, to avoid redundant ones
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


def z3_eq(z3_var, value) -> BoolRef:
    if isinstance(value, list):
        constraints = [Length(z3_var) == len(value)]
        for i in range(len(value)):
            constraint = z3_var[i] == value[i]
            constraints.append(constraint)
        return And(constraints)

    return z3_var == value


def _check_positive_examples_satisfy_property(positive_examples: List[Dict[str, Any]],
                                              property_to_prove: BoolRef) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    If one of the positive examples does not agree with the property that we want to prove, then we
    can't possibly find a formula that agrees on the positive examples and implies the property. So we do this check
    to make sure we are not chasing our own tails
    """
    for example in positive_examples:
        constraints = [property_to_prove]

        for variable, value in example.items():
            variable_z3 = var_to_z3(variable, type(value))
            # TODO: make sure that this works for arrays and strings
            constraint = z3_eq(variable_z3, value)
            constraints.append(constraint)

        property_with_constraints = And(constraints)
        s = Solver()
        s.add(property_with_constraints)
        res = s.check()
        assert res != unknown, "cannot deal with unknown check result."
        if res == unsat:
            return False, example

    return True, None


class SynthesisResult:
    def __init__(self, success: bool, bad_property: bool, timeout: bool, value=None):
        assert value is not None or not success, "if success, result must be provided."
        self.success = success
        self.bad_property = bad_property
        self.timeout = timeout
        self.value = value

    @classmethod
    def timeout_cons(cls):
        return cls(False, False, True)

    @classmethod
    def bad_property_cons(cls, bad_example):
        # TODO: return also the bad example that does not satisfy the constraint
        return cls(False, True, False, bad_example)

    @classmethod
    def success_cons(cls, result: BoolRef):
        return cls(True, False, False, result)


def counter_example_synthesis(positive_examples: List[Dict[str, Any]], functions: List[Callable], constants: List,
                              property_to_prove: BoolRef,
                              max_counter_examples=config.MAX_COUNTER_EXAMPLES_ROUNDS) -> SynthesisResult:

    all_examples_good, bad_example = _check_positive_examples_satisfy_property(positive_examples, property_to_prove)
    if not all_examples_good:
        return SynthesisResult.bad_property_cons(bad_example)

    var_name_to_type = {name: type(value) for name, value in positive_examples[0].items()}
    negative_examples = []

    for counter_example_i in range(max_counter_examples):
        assumption = find_satisfying_expr(positive_examples, negative_examples, functions, constants)
        counter_example = _find_counter_example(assumption, property_to_prove, var_name_to_type)
        if counter_example.counter_example_found:
            negative_examples.append(counter_example.example)
        else:
            return SynthesisResult.success_cons(assumption)

    return SynthesisResult.timeout_cons()


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

    # TODO: deal with unknown
    if res == unknown:
        raise RuntimeError(f"cannot deal with unknown")

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
                s_val = value.as_string()
                value = value.as_long()
            elif t == str:
                value = value.as_string()
            elif t == list:
                value = _z3_array_to_list(value, model)
            else:
                assert False, f"Does not support {t}"

            counter_example[var_name] = value

    return _CounterExampleResult.counter_example(example=counter_example)
