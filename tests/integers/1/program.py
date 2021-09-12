def test(x: int, y: int, z: int):
    while z * 2 > x + y:
        x = y
        y = y + 1
