import pandas as pd

from comchoice.aggregate.condorcet import condorcet


def weak_condorcet(
    df,
    candidate="candidate",
    rank="rank",
    delimiter=">",
    voter="voter",
    voters="voters"
):
    return condorcet(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        weak=True
    )
