import pandas as pd

# from .comchoice.aggregage.condorcet import condorcet


def condorcet():
    return


def pareto(
    df,
    selected="selected",
    voter="voter"
):
    """
    Pareto: Dominated alternatives can not win.
    There are multiple winners. 
    Other utility function should be used to find a unique winner.

    Returns
    -------
    bool: 
        Boolean variable to indicate if the data is complete.
    """

    if condorcet(df):
        return False

    tmp = df.groupby(voter)[selected].value_counts(normalize=True)
    n_unique_winners = tmp.nlargest(1, keep="all")\
        .reset_index(drop=True)[selected].nunique()

    return n_unique_winners > 1
