from z3 import Function, IntSort, Solver, IntVector, Int

Z = IntSort()
f = Function('f', Z, Z)
s = Solver()
s.add(f(0) == 1, f(1) == 1, f(2) == 0, f(3) == 3)
s.check()
m = s.model()

#%%
r = m[f]

#%%
dir(r)

#%%
print(r)
print(r.as_list())

sz = Int('sz')
X = IntVector('x', sz)
print(X)