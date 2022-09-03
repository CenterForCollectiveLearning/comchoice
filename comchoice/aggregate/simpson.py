import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.minimax import minimax


def simpson(
    df,
    method: str = "winning_votes",
    alternative: str = "alternative",
    ballot: str = "ballot",
    delimiter: str = ">",
    show_rank: bool = True,
    voter: str = "voter",
    voters: str = "voters",
    transform_kws: dict = transform_kws
):
    return minimax(
        df,
        method=method,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        show_rank=show_rank,
        voter=voter,
        voters=voters,
        transform_kws=transform_kws
    )
