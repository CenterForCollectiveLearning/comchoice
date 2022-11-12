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
    set_transform=True,
    transform_kws=transform_kws
):
    """Pairwise Matrix.

    Parameters
    ----------
    df : pd.DataFrame
        _description_
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    voter : str, optional
        _description_, by default "voter"
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".
    return_alternatives : bool, optional
        Whether the value is `True`, it returns a second variable that includes the alternatives's labels, by default False.
    set_transform : bool, optional
        Whether the value is `True`, it converts the DataFrame into a Pairwise object, by default True.
    transform_kws : dict, optional
        Whether or not to process data.

    Returns
    -------
    pd.DataFrame
        _description_

    """
    output = []

    cols = ["_winner", "_loser"]

    if set_transform:
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
