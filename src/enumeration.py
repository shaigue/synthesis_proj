"""
In this work we assume a very simple grammar, similar to FOL.
The grammar contains functions, variables, and constants.
Height 0 contains the constants and the variables, and functions are applied to increase the depth.
"""
import inspect
import itertools
import logging
from collections import defaultdict
from typing import List, Callable, Any, Dict, Tuple, Type, Set

from z3 import Int, String, IntVal, StringVal, Z3Exception

from src.utils.int_seq_utils import IntSeq
# from src.library.int_seq import int_seq_select


def bottom_up_enumeration_with_observational_equivalence(examples: List[Dict[str, Any]], functions: List[Callable],
                                                         constants: List[Any], max_depth: int, ignore_vars: Set[str]):
    typed_value_vector_to_expr = _init_value_vector_to_expr(examples, constants, ignore_vars)

    for depth in range(max_depth):
        new_typed_value_vector_to_expr = defaultdict(dict)

        for func in functions:
            for value_vector_list, expr_list in _iter_params(func, typed_value_vector_to_expr):
                value_vector = tuple(func(*params) for params in zip(*value_vector_list))

                t = _get_func_ret_type(func)

                if value_vector not in typed_value_vector_to_expr[t] and \
                        value_vector not in new_typed_value_vector_to_expr[t]:
                    expr = func(*expr_list, to_z3=True)
                    if t == list:
                        value_vector = tuple(tuple(val) for val in value_vector)
                    new_typed_value_vector_to_expr[t][value_vector] = expr
                    yield value_vector, expr, t

        if len(new_typed_value_vector_to_expr) == 0:
            return

        for t, new_value_vector_to_expr in new_typed_value_vector_to_expr.items():
            if t in typed_value_vector_to_expr:
                typed_value_vector_to_expr[t].update(new_value_vector_to_expr)
            else:
                typed_value_vector_to_expr[t] = new_value_vector_to_expr


def _get_func_ret_type(func: Callable) -> Type:
    func_sig = inspect.signature(func)
    return func_sig.return_annotation


def _iter_params(func: Callable, typed_value_vector_to_expr: Dict[Type, Dict[Tuple, str]]):
    """Assumes that the functions are annotated with types, and the last parameter is "to_z3"."""
    func_sig = inspect.signature(func)
    product_sets = []
    for param in list(func_sig.parameters.values())[:-1]:
        t = param.annotation
        product_sets.append(typed_value_vector_to_expr[t].items())

    for value_vector_expr_pair_list in itertools.product(*product_sets):
        value_vector_list = []
        expr_list = []

        for value_vector, expr in value_vector_expr_pair_list:
            value_vector_list.append(value_vector)
            expr_list.append(expr)

        yield value_vector_list, expr_list


def _const_to_z3(constant):
    t = type(constant)
    if t == int:
        return IntVal(constant)
    if t == str:
        return StringVal(constant)
    raise NotImplementedError(f"type {t} is not supported")


def var_to_z3(name: str, t: Type):
    if t == int:
        return Int(name)
    if t == str:
        return String(name)
    if t == list:
        return IntSeq(name)
    raise NotImplementedError(f"type {t} is not supported")


def _init_value_vector_to_expr(examples: List[Dict[str, Any]], constants: List, ignore_vars: Set[str]):
    typed_value_vector_to_expr = defaultdict(dict)

    for constant in constants:
        value_vector = (constant,) * len(examples)
        t = type(value_vector[0])
        if value_vector not in typed_value_vector_to_expr[t]:
            typed_value_vector_to_expr[t][value_vector] = _const_to_z3(constant)

    variables = set()
    for example in examples:
        variables.update(example.keys())

    variables.difference_update(ignore_vars)

    for variable in variables:
        value_vector = tuple(example[variable] for example in examples)
        t = type(value_vector[0])
        if t == list:
            value_vector = tuple(tuple(example[variable]) for example in examples)
        if value_vector not in typed_value_vector_to_expr[t]:
            typed_value_vector_to_expr[t][value_vector] = var_to_z3(variable, t)

    return typed_value_vector_to_expr
