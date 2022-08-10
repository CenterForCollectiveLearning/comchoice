import numpy as np
import pandas as pd


def __set_card_id(
    df,
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    selected="selected",
    concat: str = "_"
) -> pd.DataFrame:
    """Creates a unique identifier for alternatives' pair (card_id).

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

    alternative_a_sorted = f"{alternative_a}_sorted"
    alternative_b_sorted = f"{alternative_b}_sorted"

    cols = [alternative_a, alternative_b, selected]
    a = df[cols].values

    # Sorts options, always lower value on left column
    df[alternative_a_sorted] = np.where(a[:, 0] < a[:, 1], a[:, 0], a[:, 1])
    df[alternative_b_sorted] = np.where(a[:, 0] >= a[:, 1], a[:, 0], a[:, 1])

    _a = df[alternative_a_sorted]
    _b = df[alternative_b_sorted]

    df["option_selected"] = np.where(
        _a[:] == a[:, 2], 1, np.where(_b[:] == a[:, 2], -1, 0))

    # Creates card_id
    df["card_id"] = _a.astype(str) + concat + _b.astype(str)

    # Boolean variable, check if a/b was selected
    df["option_source"] = np.where(a[:, 1] == a[:, 2], a[:, 0], a[:, 1])
    df["option_target"] = np.where(a[:, 0] == a[:, 2], a[:, 0], a[:, 1])

    # Creates option_source / option_target
    selected_zero = df[selected] == 0
    df.loc[selected_zero, "option_source"] = df.loc[selected_zero, alternative_a]
    df.loc[selected_zero, "option_target"] = df.loc[selected_zero, alternative_b]

    df["id"] = range(1, df.shape[0] + 1)

    return df
