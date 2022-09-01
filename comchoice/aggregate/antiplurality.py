import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.plurality import plurality


def antiplurality(
    df,
    alternative="alternative",
    delimiter=">",
    ballot="ballot",
    show_rank=True,
    voters="voters",
    transform_kws=transform_kws
) -> pd.DataFrame:
    return plurality(
        df,
        alternative=alternative,
        delimiter=delimiter,
        ballot=ballot,
        show_rank=show_rank,
        voters=voters,
        ascending=True,
        transform_kws=transform_kws
    )
