import pandas as pd


def faithfulness(
    df,
    options,
    selected="selected"
):
    """
    Faithfulness: There is only one winner when considering just one voter.
    There is no absent vote. Each vote would elect someone.

    Returns
    -------
    bool:
        Boolean variable to indicate if the data is complete.
    """

    return len(df[~df[selected].isin(options)]) == 0
