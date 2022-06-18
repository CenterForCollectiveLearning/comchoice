import numpy as np
import pandas as pd


def __set_card_id(
    df,
    candidate_a="candidate_a",
    candidate_b="candidate_b",
    selected="selected",
    concat: str = "_"
) -> pd.DataFrame:
    """Creates a unique identifier for candidates' pair (card_id).

    Parameters
    ----------
    df : pandas.DataFrame
        Pairwise comparison DataFrame.

    concat : str, default="_"
        String to concatenate options.

    Returns
    -------
    pd.DataFrame
        A pairwise comparison DataFrame with card_id column.
    """

    option_a_sorted = f"{candidate_a}_sorted"
    option_b_sorted = f"{candidate_b}_sorted"

    cols = [candidate_a, candidate_b, selected]
    a = df[cols].values

    # Sorts options, always lower value on left column
    df[option_a_sorted] = np.where(a[:, 0] < a[:, 1], a[:, 0], a[:, 1])
    df[option_b_sorted] = np.where(a[:, 0] >= a[:, 1], a[:, 0], a[:, 1])

    _a = df[option_a_sorted]
    _b = df[option_b_sorted]

    df["option_selected"] = np.where(
        _a[:] == a[:, 2], 1, np.where(_b[:] == a[:, 2], -1, 0))

    # Creates card_id
    df["card_id"] = _a.astype(str) + concat + _b.astype(str)

    # Boolean variable, check if a/b was selected
    df["option_source"] = np.where(a[:, 1] == a[:, 2], a[:, 0], a[:, 1])
    df["option_target"] = np.where(a[:, 0] == a[:, 2], a[:, 0], a[:, 1])

    # Creates option_source / option_target
    selected_zero = df[selected] == 0
    df.loc[selected_zero, "option_source"] = df.loc[selected_zero, candidate_a]
    df.loc[selected_zero, "option_target"] = df.loc[selected_zero, candidate_b]

    df["id"] = range(1, df.shape[0] + 1)

    return df
