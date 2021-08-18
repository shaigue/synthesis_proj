from z3 import *

# A = Array('A', IntSort(), IntSort())
# x, y = Ints('x y')
# solve(A[x] == y, Store(A, x, y) == A)

# p, q, r = Bools('p q r')
# s = Solver()
# s.add(Implies(p, q))
# s.add(Not(q))
# print(s.check())
# print(s.check(p))
# s.push()
# s.add(p)
# print(s.check())
# s.pop()
# print(s.check())

# p, q, r, v = Bools('p q r v')
# s = Solver()
# s.add(Not(q))
# s.assert_and_track(q, p)
# s.assert_and_track(r, v)
# print(s.check())
# print(s.unsat_core())

# Z = IntSort()
# f = Function('f', Z, Z)
# x, y = Ints('x y')
# s = Solver()
# s.add(f(x) > y, f(f(y)) == y)
# print(s.check())
# print(s.model())
# m = s.model()
# for d in m:
#     print(d, m[d])

