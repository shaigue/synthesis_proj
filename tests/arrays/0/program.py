def get_inputs():
    import random
    return [[random.randrange(100) for _ in range(5)] for _ in range(5)]


def test(a):
    from library.arrays import _store

    _states = []
    i = 0
    while i < len(a):
        # a[i] *= 2
        a = _store(a, a[i] * 2, i)
        i += 1

    return _states


_states = []
for inp in get_inputs():
    _states += test(inp)
