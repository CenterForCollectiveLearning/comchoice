import pandas as pd

from comchoice.aggregate.dodgson_quick import dodgson_quick
from comchoice.aggregate.tideman import tideman


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
