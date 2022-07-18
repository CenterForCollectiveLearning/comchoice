import pandas as pd
from comchoice.aggregate.nanson_baldwin import nanson_baldwin


def nanson(
    df,
    alternative="alternative",
    delimiter=">",
    rank="rank",
    borda_score="original",
    show_rank=True,
    voters="voters"
) -> pd.DataFrame:

    return nanson_baldwin(
        df,
        method="nanson",
        alternative=alternative,
        delimiter=delimiter,
        rank=rank,
        borda_score=borda_score,
        show_rank=show_rank,
        voters=voters
    )
