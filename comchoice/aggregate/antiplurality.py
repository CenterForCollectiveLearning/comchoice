import pandas as pd
from .plurality import plurality


def antiplurality(
    df,
    candidate="candidate",
    delimiter=">",
    rank="rank",
    show_rank=True,
    voters="voters"
) -> pd.DataFrame:
    return plurality(
        df,
        candidate=candidate,
        delimiter=delimiter,
        rank=rank,
        show_rank=show_rank,
        voters=voters,
        ascending=True
    )
