import numpy as np
import pandas as pd
from tqdm import tqdm


def to_pairwise(
    df,
    candidate="candidate",
    option_a="option_a",
    option_b="option_b",
    selected="selected",
    value="value",
    voter="voter",
    type="star",
    verbose=True
) -> pd.DataFrame:
    """Converts a star rating dataset to a pairwise comparison dataset.

    Parameters
    ----------
    df : _type_
        _description_
    candidate : str, optional
        _description_, by default "candidate"
    option_a : str, optional
        _description_, by default "option_a"
    option_b : str, optional
        _description_, by default "option_b"
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
            f"{candidate}_x": option_a,
            f"{candidate}_y": option_b
        }
    )

    tmp[selected] = np.where(
        tmp[f"{value}_x"] == tmp[f"{value}_y"], 0,
        np.where(tmp[f"{value}_x"] > tmp[f"{value}_y"],
                 tmp[option_a], tmp[option_b])
    )

    return tmp[[voter, option_a, option_b, selected]]
