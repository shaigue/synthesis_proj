# Synthesis Project, 2021
This project is a loop invariant synthesis tool, that works on python integers, strings and list.
## Run Benchmarks
To run the benchmarks, simply execute the file `run_tests.py` from the top directory. 


## Benchmarks Results
After running the benchmarks, results will be documented under the `tests_results` directory.

The Loop Invariant generated in each test is printed to a file with the name pattern `<group name>_<test name>.txt`. For example, the corresponding file of test 2 of the integers tests is `int_tests_test_2.txt`.

Additionally, a file containing a table with the tests results is generated for each benchmark group - `int_tests.txt`, `str_tests.txt` and `int_seq_tests.txt`. The table includes the following information for each test in the group:
* Result - either success (a loop invariant was found and the property was proven), timeout, or "bad property" (i.e. the property is incorrect, and one of the positive examples disproves it). A timeout can happen if the time limit is reached, if the depth limit of the enumerator is reached, or if the iterations limit of the CEGIS loop is reached.
* Runtime - For how long did the test run, in seconds. 
* Is correct - The property to prove is correct and the loop invariant can be expressed with the given grammar. 
* Is expressible - The property to prove is correct, but the necessary loop invariant cannot be generated using the given grammar.

## Tool's Input
### Grammar
The grammar files are under `src/library`. The tool takes a grammar as a set of type-annotated functions. Applications of a grammar derivation rule is in fact an application of one of these functions. The tool iterates over the given functions and applies them on the appropriate previously generated expressions according to the function's type annotation and the types of the expression. 
For example, a logical `or` operation is represented by the function:
```
def or_(x: bool, y: bool, to_z3=False) -> bool:
    if to_z3:
        return Or(x, y)
    return x or y
```
Note that these functions can evaluate the resulting expression (for the sake of observational equivalence) as well as create a z3 expression for the purpose of generating the loop invariant as a z3 expression. Expanding the derivation rules is a matter of defining a function in the appropriate file. 

Constants for each grammar are supplied by a `get_constants` function that returns a list of constants. 
### Benchmarks
This project contains 3 benchmark groups, each one with its own python file under the `benchmarks` directory:
* `int_tests.py` - Contains 6 integers benchmarks
* `str_tests.py` - Contains 6 strings benchmarks
* `int_seq_tests.py` - Contains 6 lists benchmarks

Each test is a function that returns a `Benchmark` object that includes:
* A function with a single loop
* Property to prove as a z3 expression
* Optional limitations on the inputs to be randomly generated
* The test's classification.

Each test can be classified as one of the following three:
* Correct (explained above)
* Not expressible (explained above)
* Incorrect - The given property is not correct for the given program, i.e. a buggy program.


## Test Case
`test_3` in `int_seq_tests` benchmark group: This test creates gets two lists `l1`, `l2` as inputs, and calculates in a variable `m` the minimal value of `l1` and `l2`. The synthesize shows that there exists an index `i1` such that `l1[i1] == m` or that there exists an index `i2` such that `l2[i2] == m`. In our test run, the synthesize solved this test in 8.8 seconds. 

## Notable Techniques
We use some notable techniques in our tool:
* CEGIS Loop - Instead of manually writing the negative examples for each benchmark, the tool starts its work on a test by generating only the positive examples (by randomly generating inputs for the test and executing it), and then it executes a CEGIS loop. This means that the negative examples are generated from the z3 solver model for the formula `Not(Implies(loop_inv, property))`. After each attempt the tool collects the negative example from the z3 model, and tries to generate another loop invariant candidate that will evaluate to true on all positive examples, and to false on all negative examples.
* Conjunctions - The tool collects loop invariant candidates that evaluate to true on all positive examples but doesn't necessarily evaluate to false on all negative examples. It then tries to find a group of candidates that "cover" among them all of the negative examples, i.e. it finds a group of candidates such that for each negative example, at least one candidate evaluates to false. The tool then creates a conjunction of all the candidates and tests it in the CEGIS loop as a possible loop invariant. This allows us to decrease runtime, as well as generate more complex expressions without letting the enumerator reaching to depths in which a search would be inefficient.
