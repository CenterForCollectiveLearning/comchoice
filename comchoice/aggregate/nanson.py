import pandas as pd
from . import nanson_baldwin


def nanson(
    df,
    candidate="candidate",
    delimiter=">",
    rank="rank",
    borda_score="original",
    show_rank=True,
    voters="voters"
) -> pd.DataFrame:

    return nanson_baldwin(
        df,
        method="nanson",
        candidate=candidate,
        delimiter=delimiter,
        rank=rank,
        borda_score=borda_score,
        show_rank=show_rank,
        voters=voters
    )
