"""
Module for automatic negative states creation.
The idea is to make the loop invariant synthesis an iterative process. Initialize with:
* set of positive states PS
* empty set of negative states NS
* safety property that we need to prove SP

In each iteration:
1. synthesis a loop invariant LI, such that each state in PS is true and each state in NS is false
2. check if LI => SP (i.e. the safety property can be proved), if so, terminate
3. generate a new counterexample by searching for a model that satisfies (LI and (not SP)), i.e. a state that satisfies
    the loop invariant and not the safety property. Add this state to the negative samples.
"""

# TODO: discuss Asaf this, and how should this be done
