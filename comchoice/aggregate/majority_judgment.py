import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.judgment import judgment


def majority_judgment(
    df: pd.DataFrame,
    alternative: str = "alternative",
    ballot: str = "ballot",
    delimiter: str = ">",
    dtype: str = "ballot",
    ratings=None,
    show_rank: bool = True,
    transform_kws: dict = transform_kws,
    voters: str = "voters",
    e: int = 0
):
    return judgment(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        dtype=dtype,
        method="majority",
        ratings=ratings,
        show_rank=show_rank,
        transform_kws=transform_kws,
        voters=voters,
        e=e
    )
