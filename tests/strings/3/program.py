def get_inputs():
    import random
    from config import _NUM_INPUTS

    xs = [random.randrange(50) for _ in _NUM_INPUTS]
    ys = [x + random.randrange(1, 50) for x in xs]
    return list(zip(xs, ys))


def test(x, y):
    s = "x"
    while x < y:
        y = y - 1
        s = s + 'a'
