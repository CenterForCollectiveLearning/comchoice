import numpy as np
import pandas as pd
from itertools import combinations


def pairwise_matrix(
    df,
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    voter="voter",
    voters="voters",
    return_alternatives=False
):
    output = []

    cols = ["_winner", "_loser"]

    def __transform(data, unique_id=False) -> pd.DataFrame:
        df = data.copy()
        df["_id"] = range(df.shape[0])
        df[ballot] = df[ballot].str.split(delimiter)
        df = df.explode(rank)
        df = df.rename(columns={rank: "alternative"})
        df["rank"] = df.groupby("_id").cumcount() + 1
        if not unique_id:
            df = df.drop(columns=["_id"])

        return df

    df = __transform(df, unique_id=True)
    if voters in list(df):
        df = df.rename(columns={"_id": "voter"})
    else:
        df[voters] = 1

    unique_alternatives = df[alternative].unique()
    for idx, df_tmp in df.groupby([voter, voters]):
        _voter, _voters = idx

        df_tmp = df_tmp.sort_values("rank")
        items = df_tmp[alternative].values

        tmp = pd.DataFrame(list(combinations(items, 2)), columns=cols)
        tmp["value"] = _voters
        output.append(tmp)

    m = pd.concat(output).groupby(cols).agg({"value": "sum"}).reset_index()

    m = m.pivot(index=cols[0], columns=cols[1], values="value")
    m = m.reindex(unique_alternatives, axis=0)
    m = m.reindex(unique_alternatives, axis=1)
    m = m.fillna(0)

    if return_alternatives:
        return m, unique_alternatives

    return m
