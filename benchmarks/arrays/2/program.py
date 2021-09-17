def get_inputs():
    import random
    from config import N_INPUTS
    return [[random.randrange(-100, 100) for _ in range(5)] for _ in range(N_INPUTS)]


def test(a):
    m = 0
    i = 0
    while i < len(a):
        if m < a[i]:
            m = a[i]
        i += 1
