import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.aggregate.__transform import __transform


def k_approval(
    df,
    k=1,
    candidate="candidate",
    rank="rank",
    show_rank=True,
    voters="voters"
) -> pd.DataFrame:
    """k-Approval voting method.

    The method gives 1 if the candidate is ranked over or equal to k. Otherwise, the value given is 0.

    Parameters
    ----------
    k (int, default=1, optional):
        Threshold to score candidates with a value of 1.

    Returns
    -------
    pandas.DataFrame:
        Election results using the k-approval method.

    References
    ----------

    """
    # if plural_voters:
    df = __transform(df)
    df["value"] = df[rank] <= k

    df = __set_voters(df, voters=voters)
    df = __aggregate(df, groupby=[candidate], aggregation="sum")

    if show_rank:
        df = __set_rank(df)

    return df
