import pandas as pd


def cancellation(
    data,
    voter="voter",
    selected="selected"
):
    """
    Cancellation: all tied alternatives in the 
    top-ranked position will win.

    Returns
    -------
    bool: 
        Boolean variable to indicate if the data is complete.
    """

    tmp = data.groupby(voter)[selected].value_counts(normalize=True)
    n_unique_winners = tmp.nlargest(1, keep="all")\
        .reset_index(drop=True)[selected].nunique()

    return n_unique_winners > 1
