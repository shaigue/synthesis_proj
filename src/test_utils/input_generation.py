import random
from inspect import signature
from typing import List, Callable, Union, Dict, Type

# random.seed(42)
MIN_ARR_LEN = 0
MAX_ARR_LEN = 10
MIN_STR_LEN = 0
MAX_STR_LEN = 10
MIN_STR_CHAR_ORD = ord('A')
MAX_STR_CHAR_ORD = ord('Z')
MIN_INT_VALUE = -100
MAX_INT_VALUE = 100


def get_random_int(min_value=MIN_INT_VALUE, max_value=MAX_INT_VALUE) -> int:
    return random.randint(min_value, max_value)


def get_random_str(min_str_len=MIN_STR_LEN, max_str_len=MAX_STR_LEN, min_str_char_ord=MIN_STR_CHAR_ORD,
                   max_str_char_ord=MAX_STR_CHAR_ORD) -> str:
    str_len = random.randint(min_str_len, max_str_len)
    s = ''
    for i in range(str_len):
        char_ord = random.randint(min_str_char_ord, max_str_char_ord)
        char = chr(char_ord)
        s += char
    return s


def get_random_arr(min_arr_len=MIN_ARR_LEN, max_arr_len=MAX_ARR_LEN, min_value=MIN_INT_VALUE,
                   max_value=MAX_INT_VALUE) -> List[int]:
    arr_len = random.randint(min_arr_len, max_arr_len)
    return [random.randint(min_value, max_value) for _ in range(arr_len)]


def get_random_param(t: Type):
    if t == int:
        return get_random_int()
    if t == str:
        return get_random_str()
    if t == List[int]:
        return get_random_arr()
    assert False, f"type {t} is not supported."


def generate_input_for_program(program: Callable) -> Dict[str, Union[int, str, List[int]]]:
    """
    Assumes that program has type annotations for parameters.

    returns: a mapping from input parameter to its value.
    """
    sig = signature(program)
    params = {}
    for param_name, param_data in sig.parameters.items():
        t = param_data.annotation
        param_value = get_random_param(t)
        params[param_name] = param_value
    return params


def example():
    def program(x: int, y: int, s: str, a: List[int]):
        print(x)
        print(y)
        print(s)
        print(a)

    inputs = generate_input_for_program(program)
    program(**inputs)


if __name__ == '__main__':
    example()