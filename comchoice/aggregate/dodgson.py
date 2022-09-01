import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.dodgson_quick import dodgson_quick
from comchoice.aggregate.tideman import tideman


def dodgson(
    df,
    approximation="quick",
    alternative="alternative",
    delimiter=">",
    ballot="ballot",
    show_rank=True,
    voter="voter",
    voters="voters",
    transform_kws=transform_kws
):
    if approximation == "quick":
        return dodgson_quick(
            df,
            alternative=alternative,
            delimiter=delimiter,
            ballot=ballot,
            show_rank=show_rank,
            voter=voter,
            voters=voters,
            transform_kws=transform_kws
        )
    elif approximation == "tideman":
        return tideman(
            df,
            alternative=alternative,
            delimiter=delimiter,
            ballot=ballot,
            show_rank=show_rank,
            voter=voter,
            voters=voters,
            transform_kws=transform_kws
        )
