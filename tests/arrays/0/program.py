from src.library.arrays import _store

a = [1, 2, 3, 4, 5]
i = 0
while i < len(a):
    # a[i] *= 2
    a = _store(a, a[i] * 2, i)
    i += 1
