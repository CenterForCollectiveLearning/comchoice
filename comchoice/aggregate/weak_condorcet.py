import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.condorcet import condorcet


def weak_condorcet(
    df,
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    voter="voter",
    voters="voters",
    transform_kws=transform_kws
):
    return condorcet(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        weak=True,
        transform_kws=transform_kws
    )
