"""
This module contains the available functions that the synthesizer can use to form
The loop invariant.
"""
from typing import List, Dict, Any
from . import booleans, strings, integers, int_seq
import z3


def _get_module_functions(module):
    functions = dir(module)
    functions = filter(lambda x: not x.startswith('_'), functions)
    functions = filter(lambda x: not x.startswith('get_'), functions)
    functions = filter(lambda x: not x.isupper(), functions)
    z3_functions = dir(z3)
    functions = set(functions).difference(z3_functions)
    return [getattr(module, func_name) for func_name in functions]


def get_bool_functions():
    return _get_module_functions(booleans)


def get_int_functions_and_constants():
    functions = get_bool_functions() + _get_module_functions(integers)
    constants = integers.get_constants()
    return functions, constants


def get_string_functions_and_constants():
    int_funcs, int_consts = get_int_functions_and_constants()
    functions = int_funcs + _get_module_functions(strings)
    constants = int_consts + strings.get_constants()
    return functions, constants


def get_array_functions_and_constants():
    int_funcs, int_consts = get_int_functions_and_constants()
    functions = int_funcs + _get_module_functions(int_seq)
    constants = int_consts + int_seq.get_constants()
    return functions, constants


def get_functions_and_constants(examples: List[Dict[str, Any]]):
    has_str = False
    has_arr = False
    for example in examples:
        for value in example.values():
            if isinstance(value, str):
                has_str = True
            if isinstance(value, list):
                has_arr = True
    if has_str and has_arr:
        raise RuntimeError("strings and arrays together are not supported.")
    if has_str:
        return get_string_functions_and_constants()
    if has_arr:
        return get_array_functions_and_constants()
    return get_int_functions_and_constants()
