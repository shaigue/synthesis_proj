from z3 import SeqSort, IntSort, Const, Solver, Length, sat

IntArr = SeqSort(IntSort())
x = Const('x', IntArr)
s = Solver()
s.add(x[0] == 1, x[1] == 2, x[2] == 3, Length(x) == 10)
res = s.check()
if res == sat:
    m = s.model()
    for d in m:
        # print(d)
        z = m[d]
        v1 = z[1]
        b = v1 > 1
        b1 = m.evaluate(b)
        v2 = m.evaluate(v1)
        print(v1)
