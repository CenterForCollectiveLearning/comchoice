import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.judgment import judgment


def typical_judgment(
    df,
    alternative="alternative",
    ballot="rank",
    delimiter=">",
    dtype="ballot",
    ratings=None,
    show_rank=True,
    transform_kws=transform_kws,
    voters="voters",
    e=0
):
    return judgment(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        dtype=dtype,
        method="typical",
        ratings=ratings,
        show_rank=show_rank,
        transform_kws=transform_kws,
        voters=voters,
        e=e
    )
