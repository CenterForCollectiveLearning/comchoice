import numpy as np
import pandas as pd


def _create_card_id(df):
    """
    Creates a new column called "card_id".
    Format: 1 + <proposal_id> + <proposal_id>.

    Parameters:
        df (DataFrame)
    """
    cols = ["option_a", "option_b", "selected"]
    a = df[cols].values

    # Sorts options, always lower value on left column
    df["option_a_sorted"] = np.where(a[:, 0] < a[:, 1], a[:, 0], a[:, 1])
    df["option_b_sorted"] = np.where(a[:, 0] >= a[:, 1], a[:, 0], a[:, 1])

    _a = df["option_a_sorted"]
    _b = df["option_b_sorted"]

    # df["option_selected"] = df.apply(lambda x: 1 if x["option_a_sorted"] == x["selected"] else -1 if x["option_b_sorted"] == x["selected"] else 0, axis=1)
    df["option_selected"] = np.where(_a[:] == a[:, 2], 1, np.where(_b[:] == a[:, 2], -1, 0))

    # Generates a card id
    df["card_id"] = df["option_a_sorted"].astype(str) + "_" + df["option_b_sorted"].astype(str)

    # Boolean variable, check if a/b was selected
    df["option_source"] = np.where(a[:, 1] == a[:, 2], a[:, 0], a[:, 1])
    df["option_target"] = np.where(a[:, 0] == a[:, 2], a[:, 0], a[:, 1])

    # Creates option_source / option_target
    selected_zero = df["selected"] == 0
    df.loc[selected_zero, "option_source"] = df.loc[selected_zero, "option_a"]
    df.loc[selected_zero, "option_target"] = df.loc[selected_zero, "option_b"]

    return df