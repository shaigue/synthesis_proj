from z3 import IntSort, SeqSort, Const


def IntSeq(name: str):
    IntSeqSort = SeqSort(IntSort())
    return Const(name, IntSeqSort)

