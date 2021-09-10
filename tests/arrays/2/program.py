def get_inputs():
    import random
    return [[random.randrange(-100, 100) for _ in range(5)] for _ in range(5)]


def test(a):
    _states = []
    m = 0
    i = 0
    while i < len(a):
        if m < a[i]:
            m = a[i]
        i += 1

    return _states


_states = []
for inp in get_inputs():
    _states += test(inp)
