import pandas as pd
from comchoice.aggregate.plurality import plurality


def antiplurality(
    df,
    alternative="alternative",
    delimiter=">",
    rank="rank",
    show_rank=True,
    voters="voters"
) -> pd.DataFrame:
    return plurality(
        df,
        alternative=alternative,
        delimiter=delimiter,
        rank=rank,
        show_rank=show_rank,
        voters=voters,
        ascending=True
    )
