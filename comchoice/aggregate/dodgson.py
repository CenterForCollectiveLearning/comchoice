import pandas as pd

from . import dodgson_quick, tideman


def dodgson(
    df,
    approximation="quick",
    candidate="candidate",
    delimiter=">",
    rank="rank",
    show_rank=True,
    voter="voter",
    voters="voters"
):
    if approximation == "quick":
        return dodgson_quick(
            df,
            candidate=candidate,
            delimiter=delimiter,
            rank=rank,
            show_rank=show_rank,
            voter=voter,
            voters=voters
        )
    elif approximation == "tideman":
        return tideman(
            df,
            candidate=candidate,
            delimiter=delimiter,
            rank=rank,
            show_rank=show_rank,
            voter=voter,
            voters=voters
        )
