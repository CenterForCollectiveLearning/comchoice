import pandas as pd

from comchoice.aggregate.condorcet import condorcet


def weak_condorcet(
    df,
    alternative="alternative",
    rank="rank",
    delimiter=">",
    voter="voter",
    voters="voters"
):
    return condorcet(
        df,
        alternative=alternative,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        weak=True
    )
