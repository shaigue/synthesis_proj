def get_inputs():
    import random
    from config import _NUM_INPUTS
    return [[random.randrange(1, 100) for _ in range(5)] for _ in range(_NUM_INPUTS)]


def test(a):
    from library.arrays import _store

    i = 0
    while i < len(a):
        # a[i] *= 2
        a = _store(a, a[i] * 2, i)
        i += 1
