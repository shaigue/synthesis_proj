from z3 import IntSort, SeqSort, Const, Array


def IntSeq(name: str):
    IntSeqSort = SeqSort(IntSort())
    return Const(name, IntSeqSort)
    # return Array(name, IntSort(), IntSort())
