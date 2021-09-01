import inspect


def func(a: str, b: int, c) -> float:
    print(a)
    return b + c

x = func
print(x.__name__)
func_sig = inspect.signature(func)
print(func_sig)
print(func_sig.parameters)
for k,v in func_sig.parameters.items():
    print(k)
    print(v)
    t = v.annotation
    print(t)

