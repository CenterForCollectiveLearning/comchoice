import pandas as pd

from comchoice.aggregate.minimax import minimax


def simpson(
    df,
    method="winning_votes",
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    show_rank=True,
    voter="voter",
    voters="voters"
):
    return minimax(
        df,
        method=method,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        show_rank=show_rank,
        voter=voter,
        voters=voters
    )
