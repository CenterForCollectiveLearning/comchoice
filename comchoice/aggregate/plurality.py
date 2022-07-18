import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.aggregate.__transform import __transform


def plurality(
    df,
    alternative="alternative",
    delimiter=">",
    rank="rank",
    show_rank=True,
    voters="voters",
    ascending=False
) -> pd.DataFrame:
    """Plurality Rule.

    Each voter selects one alternative (or none if voters can abstain), and the alternative(s) with the most votes win.

    Returns
    -------
    pandas.DataFrame:
        Election results using Plurality Rule.
    """

    df = __transform(df, delimiter=delimiter)

    df = df[df[rank] == 1].copy()
    df["value"] = 1
    df = __set_voters(df, voters=voters)
    alternatives = df[alternative].unique()
    tmp = df.groupby(alternative).agg({"value": "sum"})\
        .reindex(alternatives).fillna(0)\
        .reset_index()

    if show_rank:
        tmp = __set_rank(tmp, ascending=ascending)

    return tmp
