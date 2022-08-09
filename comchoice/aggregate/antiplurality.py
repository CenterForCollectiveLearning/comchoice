import pandas as pd
from comchoice.aggregate.plurality import plurality


def antiplurality(
    df,
    alternative="alternative",
    delimiter=">",
    ballot="ballot",
    show_rank=True,
    voters="voters"
) -> pd.DataFrame:
    return plurality(
        df,
        alternative=alternative,
        delimiter=delimiter,
        ballot=ballot,
        show_rank=show_rank,
        voters=voters,
        ascending=True
    )
