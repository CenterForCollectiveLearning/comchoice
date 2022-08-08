import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import combinations


def to_pairwise(
    df,
    alternative="alternative",
    ascending=False,
    delimiter=">",
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    selected="selected",
    rank="rank",
    value="value",
    voter="voter",
    voters="voters",
    origin="star",
    verbose=True
) -> pd.DataFrame:
    """Converts a star rating dataset to a pairwise comparison dataset.

    Parameters
    ----------
    df : _type_
        _description_
    alternative : str, optional
        _description_, by default "alternative"
    alternative_a : str, optional
        _description_, by default "alternative_a"
    alternative_b : str, optional
        _description_, by default "alternative_b"
    selected : str, optional
        _description_, by default "selected"
    value : str, optional
        _description_, by default "value"
    voter : str, optional
        _description_, by default "voter"
    verbose : bool, optional
        _description_, by default True

    Returns
    -------
    pd.DataFrame
        _description_
    """

    if origin == "voting":
        if voters in list(df):
            output = []
            for i, row in df.iterrows():
                tmp = pd.DataFrame([row] * row[voters])
                output.append(tmp)
            df = pd.concat(output, ignore_index=True)
            df[voter] = range(df.shape[0])

        df[rank] = df[rank].astype(str).str.split(delimiter).apply(
            lambda x: list(combinations(x, 2)))
        df = df.explode(rank)

        df[alternative_a], df[alternative_b] = df[rank].str
        df[selected] = df[alternative_a]

        return df[[voter, alternative_a, alternative_b, selected]]

    _data_tmp = df.groupby(voter)
    _iter = tqdm(
        _data_tmp,
        position=0,
        leave=True
    ) if verbose else _data_tmp

    output = []
    for user_id, df_tmp in _iter:
        tmp = pd.merge(df_tmp, df_tmp, on=voter, how="outer")
        tmp = tmp[tmp[f"{alternative}_x"] != tmp[f"{alternative}_y"]]
        tmp = tmp[tmp[f"{alternative}_x"] > tmp[f"{alternative}_y"]]
        output.append(tmp)
        del tmp

    tmp = pd.concat(output)
    tmp = tmp.rename(
        columns={
            f"{alternative}_x": alternative_a,
            f"{alternative}_y": alternative_b
        }
    )

    if ascending:
        tmp[selected] = np.where(
            tmp[f"{value}_x"] == tmp[f"{value}_y"], 0,
            np.where(tmp[f"{value}_x"] > tmp[f"{value}_y"],
                     tmp[alternative_b], tmp[alternative_a])
        )
    else:
        tmp[selected] = np.where(
            tmp[f"{value}_x"] == tmp[f"{value}_y"], 0,
            np.where(tmp[f"{value}_x"] > tmp[f"{value}_y"],
                     tmp[alternative_a], tmp[alternative_b])
        )

    return tmp[[voter, alternative_a, alternative_b, selected]].reset_index(drop=True)
