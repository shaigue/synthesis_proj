def get_inputs():
    import random
    import string
    from config import N_INPUTS

    str_len = random.randrange(2, 100)
    letters = string.ascii_letters
    return [(''.join(random.choice(letters) for _ in range(str_len)), random.randrange(1, 100))
            for _ in range(N_INPUTS)]


def test(s, x):
    i = 2
    s1 = s[:i]
    s2 = s[i:]
    while x > 0:
        x = x - 1
        s = 'x' + s + 'y'
        s1 = 'x' + s1
        s2 = 'y' + s2
