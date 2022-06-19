import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import combinations


def to_pairwise(
    df,
    candidate="candidate",
    delimiter=">",
    candidate_a="candidate_a",
    candidate_b="candidate_b",
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
    candidate : str, optional
        _description_, by default "candidate"
    candidate_a : str, optional
        _description_, by default "candidate_a"
    candidate_b : str, optional
        _description_, by default "candidate_b"
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

        df[rank] = df[rank].str.split(delimiter).apply(
            lambda x: list(combinations(x, 2)))
        df = df.explode(rank)

        df[candidate_a] = df[rank].map(lambda x: x[0])
        df[candidate_b] = df[rank].map(lambda x: x[1])
        df[selected] = df["candidate_a"]

        return df[[voter, candidate_a, candidate_b, selected]]

    _data_tmp = df.groupby(voter)
    _iter = tqdm(
        _data_tmp,
        position=0,
        leave=True
    ) if verbose else _data_tmp

    output = []
    for user_id, df_tmp in _iter:
        tmp = pd.merge(df_tmp, df_tmp, on=voter, how="outer")
        tmp = tmp[tmp[f"{candidate}_x"] != tmp[f"{candidate}_y"]]
        tmp = tmp[tmp[f"{candidate}_x"] > tmp[f"{candidate}_y"]]
        output.append(tmp)
        del tmp

    tmp = pd.concat(output)
    tmp = tmp.rename(
        columns={
            f"{candidate}_x": candidate_a,
            f"{candidate}_y": candidate_b
        }
    )

    tmp[selected] = np.where(
        tmp[f"{value}_x"] == tmp[f"{value}_y"], 0,
        np.where(tmp[f"{value}_x"] > tmp[f"{value}_y"],
                 tmp[candidate_a], tmp[candidate_b])
    )

    return tmp[[voter, candidate_a, candidate_b, selected]]
