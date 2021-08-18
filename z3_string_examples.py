"""source: https://zyh1121.github.io/z3str3Docs/inputLanguage.html#string-primitives"""

from z3 import String, Concat, Length, SubString, PrefixOf, SuffixOf, \
    Contains, Int, IndexOf, Replace, StrToInt, IntToStr

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
# converts string representing an integer into an integer
xi = StrToInt(x)
xs = IntToStr(xi)

# TODO - there are also stuff with regexp, but I don't think that we
#   should get into that
