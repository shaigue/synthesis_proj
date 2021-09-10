from library.arrays import _store
a1 = [5, 3, 6, 2, 7]
a2 = [1, 5, 8, 4, 2]
i = 0
while i < len(a1):
    # a2[i] = a1[i]
    a2 = _store(a2, a1[i], i)
    i += 1