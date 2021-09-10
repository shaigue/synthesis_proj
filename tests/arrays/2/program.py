a = [2, 4, 2, 7, 3]
m = 0
i = 0
while i < len(a):
    if m < a[i]:
        m = a[i]
    i += 1
