# tests format
The tests are organized in the following way:
* first directory is according to the grammer for synthesizing the loop invariant
* then tests are numbered 0-9 [at most 10 tests per grammer] in a directory
* inside the test directory there are:
    1. `program.py` - the program that is to be checked
    2. `logic.json` - containes the *precondition*, *postcondition*, *loop_invariant* that can be used for proving the properties, and *correct* which signifies if the property is correct or not.
    3. `positive_states.json`, `negative_states.json` - set of positive and negative states, the input to the verifier.
