## How to change the grammar
every grammar is constructed out of functions,
and constants (variables are inferred from the examples)

- to define the constants, simply change the `get_constants()` 
function in the module
- to add a new function, just add it, and add type annotations
to every variable, and last parameter should be `to_z3=False`, 
  if this flag is true, then the function assumes that it receives z3 expressions
  instead of regular python objects, and should return a z3 expression
  