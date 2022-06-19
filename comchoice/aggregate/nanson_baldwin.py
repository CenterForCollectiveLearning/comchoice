import pandas as pd
from .borda import borda


def nanson_baldwin(
    df,
    method="nanson",
    candidate="candidate",
    delimiter=">",
    rank="rank",
    rmv=[],
    borda_score="original",
    show_rank=True,
    voters="voters"
) -> pd.DataFrame:

    rmv = []
    tmp = borda(
        df,
        candidate=candidate,
        delimiter=delimiter,
        rank=rank,
        rmv=rmv,
        score=borda_score,
        show_rank=show_rank,
        voters=voters
    )

    while tmp.shape[0] > 1:
        mean = tmp["value"].mean()
        if method == "baldwin":
            rmv += list(tmp.tail(1)[candidate].unique())
        elif method == "nanson":
            rmv += list(tmp[tmp["value"] < mean][candidate].unique())

        tmp = borda(
            df,
            candidate=candidate,
            delimiter=delimiter,
            rank=rank,
            rmv=rmv,
            score=borda_score,
            show_rank=show_rank,
            voters=voters
        )

    return tmp
