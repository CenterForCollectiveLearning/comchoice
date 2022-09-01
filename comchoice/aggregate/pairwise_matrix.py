import numpy as np
import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.preprocessing.transform import transform
from itertools import combinations


def pairwise_matrix(
    df,
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    voter="voter",
    voters="voters",
    return_alternatives=False,
    transform_kws=transform_kws
):
    output = []

    cols = ["_winner", "_loser"]

    df = transform(
        df.copy(),
        **{
            **transform_kws,
            **dict(
                ballot=ballot,
                delimiter=delimiter,
                voters=voters,
                unique_id=True
            )
        }
    )
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
