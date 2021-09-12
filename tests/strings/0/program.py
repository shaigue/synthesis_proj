def get_inputs():
    import random
    from config import N_INPUTS
    return [random.randrange(100) for _ in range(N_INPUTS)]


def test(x):
    s = ""
    i = 1
    while i < x:
        i = i + 1
        s = s + "a"
