"""source: https://zyh1121.github.io/z3str3Docs/inputLanguage.html#string-primitives"""

from z3 import String, Concat, Length, SubString, PrefixOf, SuffixOf, \
    Contains, Int, IndexOf, Replace, StrToInt, IntToStr, Solver, Strings, Implies, sat, Not, And

x = String('x')
y = String('y')
x_cat_y = Concat(x, y)
lx = Length(x)
x_eq_y = x == y
x_char_at_2 = x[2]
x_substr_1_3 = SubString(x, 1, 3)
y_prefix_of_x = PrefixOf(y, x)
y_suffix_of_x = SuffixOf(y, x)
x_contains_y = Contains(x, y)
si = Int('si')
y_starts_in_x_starting_from_si = IndexOf(x, y, si)
z = String('z')
replace_first_y_in_x_by_z = Replace(x, y, z)
xi = StrToInt(x)
xs = IntToStr(xi)

#%%
s1, s2 = Strings('s1 s2')
s = Solver()
s.add(Not(Implies(PrefixOf(s1, s2), Length(s1) <= Length(s2))))
res = s.check()
if res == sat:
    print(s.model())
else:
    print('unsat')

#%%
x, y, z = Strings('x y z')
s = Solver()
# s.add(Not(Implies(z == Concat(x, y), And(PrefixOf(x, z), SuffixOf(y, z)))))
s.add(z == Concat(x, y), Length(z) > Length(x), SuffixOf(x, z))
res = s.check()
print(f"{s} is {res}")
if res == sat:
    print(f"model - {s.model()}")

# TODO - there are also stuff with regexp, but I don't think that we
#   should get into that
