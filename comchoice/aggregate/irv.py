import pandas as pd

from comchoice.aggregate.__transform import __transform
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.aggregate.__aggregate import __aggregate


def irv(
    df,
    candidate="candidate",
    delimiter=">",
    rank="rank",
    voters="voters"
) -> pd.DataFrame:
    """Hare Rule (also called as Instant Runoff IRV, Ranked-Choice Voting, and Alternative Vote)

    Calculates the winner of an election. In each iteration,
    removes the candidate with the lowest score in a plurality rule,
    until to have a majority winner.

    Returns
    -------
    pandas.DataFrame:
        The election's winner using IRV.
    """

    df = __transform(df, delimiter=delimiter, unique_id=True)

    def __plurality(df):
        df = df[df["rank"] == 1].copy()
        df["value"] = 1
        df = __set_voters(df, voters=voters)

        return __aggregate(df, groupby=[candidate], aggregation="sum")

    tmp = __plurality(df)
    tmp["value"] /= tmp["value"].sum()
    tmp = tmp.sort_values("value", ascending=False).reset_index(drop=True)

    while tmp.loc[0, "value"] <= 0.5:
        rmv = tmp.loc[tmp.shape[0] - 1, candidate]

        df = df[df[candidate] != rmv].copy()
        df = df.sort_values(["_id", rank], ascending=[True, True])
        df[rank] = df.groupby("_id").cumcount() + 1

        tmp = __plurality(df.copy())
        tmp["value"] /= tmp["value"].sum()
        tmp = tmp.sort_values(
            "value", ascending=False).reset_index(drop=True)

    return tmp.head(1)
