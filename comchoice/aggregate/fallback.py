import pandas as pd

from comchoice.aggregate.__set_rank import __set_rank


def fallback(
    df,
    alternatives: str = "alternatives",
    delimiter: str = ">",
    delimiter_ballot: str = "|",
    voters: str = "voters"
) -> str:
    alternatives_tmp = f"{alternatives}_tmp"

    df[[alternatives, f"{alternatives}_d"]] = df[alternatives].str.split(
        delimiter_ballot, n=1, expand=True)
    df[alternatives] = df[alternatives].str.split(delimiter)

    level = 1
    W = None

    while not W:
        if voters not in list(df):
            df[voters] = 1

        n_voters = df[voters].sum()
        df[alternatives_tmp] = df[alternatives].apply(
            lambda x: x[:level]).to_list()

        tmp = df.explode(alternatives_tmp).groupby(
            alternatives_tmp).agg({voters: "sum"}) / n_voters
        tmp = tmp.reset_index()
        tmp = tmp[tmp[voters] >= 0.5].sort_values(
            voters, ascending=False).head(1)

        _W = tmp.shape[0]

        if _W == 1:
            W = tmp[alternatives_tmp].loc[0]
        else:
            level += 1

    return W
