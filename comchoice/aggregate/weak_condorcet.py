import pandas as pd

from comchoice.aggregate.condorcet import condorcet


def weak_condorcet(
    df,
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    voter="voter",
    voters="voters"
):
    return condorcet(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        weak=True
    )
