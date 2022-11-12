import pandas as pd


from comchoice.aggregate.borda import borda
from comchoice.aggregate.__default_parameters import transform_kws


def nanson_baldwin(
    df: pd.DataFrame,
    method="nanson",
    alternative="alternative",
    delimiter=">",
    ballot="ballot",
    rmv=[],
    borda_score="original",
    show_rank=True,
    voters="voters",
    transform_kws=transform_kws
) -> pd.DataFrame:

    rmv = []
    tmp = borda(
        df,
        alternative=alternative,
        delimiter=delimiter,
        ballot=ballot,
        rmv=rmv,
        score=borda_score,
        show_rank=show_rank,
        voters=voters,
        transform_kws=transform_kws
    )

    while tmp.shape[0] > 1:
        mean = tmp["value"].mean()
        if method == "baldwin":
            rmv += list(tmp.tail(1)[alternative].unique())
        elif method == "nanson":
            rmv += list(tmp[tmp["value"] < mean][alternative].unique())

        tmp = borda(
            df,
            alternative=alternative,
            delimiter=delimiter,
            ballot=ballot,
            rmv=rmv,
            score=borda_score,
            show_rank=show_rank,
            voters=voters,
            transform_kws=transform_kws
        )

    return tmp
