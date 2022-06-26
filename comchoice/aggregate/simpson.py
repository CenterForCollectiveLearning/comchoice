import pandas as pd

from comchoice.aggregate.minimax import minimax


def simpson(
    df,
    method="winning_votes",
    candidate="candidate",
    rank="rank",
    delimiter=">",
    show_rank=True,
    voter="voter",
    voters="voters"
):
    return minimax(
        df,
        method=method,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        show_rank=show_rank,
        voter=voter,
        voters=voters
    )
