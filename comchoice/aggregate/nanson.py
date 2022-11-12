import pandas as pd

from comchoice.aggregate.nanson_baldwin import nanson_baldwin
from comchoice.aggregate.__default_parameters import transform_kws


def nanson(
    df: pd.DataFrame,
    alternative="alternative",
    delimiter=">",
    ballot="ballot",
    borda_score="original",
    show_rank=True,
    voters="voters",
    transform_kws=transform_kws
) -> pd.DataFrame:

    return nanson_baldwin(
        df,
        method="nanson",
        alternative=alternative,
        delimiter=delimiter,
        ballot=ballot,
        borda_score=borda_score,
        show_rank=show_rank,
        voters=voters,
        transform_kws=transform_kws
    )
