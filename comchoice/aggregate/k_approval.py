import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.preprocessing.transform import transform


def k_approval(
    df,
    k=1,
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    show_rank=True,
    voters="voters",
    transform_kws=transform_kws,
) -> pd.DataFrame:
    """k-Approval voting method.

    The method gives 1 if the alternative is ranked over or equal to k. Otherwise, the value given is 0.

    Parameters
    ----------
    k (int, default=1, optional):
        Threshold to score alternatives with a value of 1.

    Returns
    -------
    pandas.DataFrame:
        Election results using the k-approval method.

    References
    ----------

    """
    df = transform(
        df.copy(),
        ballot=ballot,
        delimiter=delimiter,
        voters=voters,
        **transform_kws
    )
    df["value"] = df[ballot] <= k

    df = __set_voters(df, voters=voters)
    df = __aggregate(df, groupby=[alternative], aggregation="sum")

    if show_rank:
        df = __set_rank(df)

    return df
