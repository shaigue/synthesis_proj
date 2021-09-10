def get_inputs():
    import random
    return [([random.randrange(-100, 100) for _ in range(5)], [random.randrange(-100, 100) for _ in range(5)])
            for _ in range(5)]


def test(a1, a2):
    from library.arrays import _store

    _states = []
    i = 0
    while i < len(a1):
        # a2[i] = a1[i]
        a2 = _store(a2, a1[i], i)
        i += 1

    return _states


_states = []
for arr1, arr2 in get_inputs():
    _states += test(arr1, arr2)
