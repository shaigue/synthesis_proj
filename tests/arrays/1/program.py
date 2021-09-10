def get_inputs():
    import random
    from config import _NUM_INPUTS
    return [([random.randrange(-100, 100) for _ in range(5)], [random.randrange(-100, 100) for _ in range(5)])
            for _ in range(_NUM_INPUTS)]


def test(a1, a2):
    from library.arrays import _store

    i = 0
    while i < len(a1):
        # a2[i] = a1[i]
        a2 = _store(a2, a1[i], i)
        i += 1
