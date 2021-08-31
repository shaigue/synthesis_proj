s = 'ab'
s1 = 'a'
s2 = 'b'
i = 0
j = 0
t = 10
while i < t and j < t:
    if i == j:
        i = i + 1
        s = s2 + s  # i > j
    else:
        j = j + 1
        s = s1 + s  # i == j
