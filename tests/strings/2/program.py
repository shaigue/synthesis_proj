def get_inputs():
    import random
    import string
    from config import _NUM_INPUTS

    str_len = random.randrange(2, 10)
    letters = string.ascii_letters
    s1_list = [''.join(random.choice(letters) for _ in range(str_len)) for _ in range(_NUM_INPUTS)]
    s2_list = [''.join(random.choice(letters) for _ in range(str_len)) for _ in range(_NUM_INPUTS)]
    # s_list = s1_list.copy()
    s_list = [s1 + ''.join(random.choice(letters) for _ in range(str_len)) for s1 in s1_list]
    t_list = [random.randrange(10) for _ in range(_NUM_INPUTS)]
    return list(zip(s_list, s1_list, s2_list, t_list))


def test(s, s1, s2, t):
    i = 0
    j = 0
    while i < t and j < t:
        if i == j:
            i = i + 1
            s = s2 + s
        else:
            j = j + 1
            s = s1 + s
