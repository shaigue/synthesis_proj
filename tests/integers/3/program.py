def test(x: int, y: int, z: int, w: int):
    x = 0
    y = 0
    z = 0
    w = 0
    while x < 10:
        x = x + 1
        y = y - 1
        z = z + 2
        w = y
        y = z
        z = w
