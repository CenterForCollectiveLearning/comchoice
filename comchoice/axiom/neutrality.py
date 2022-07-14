import pandas as pd


def neutrality(
    data,
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    voter="voter"
):
    """
    Neutrality: all alternatives must have equal weight.
    No duplicated votes.

    Returns
    -------
    bool: 
        Boolean variable to indicate if the data is complete.
    """
    tmp = data.groupby([alternative_a, alternative_b]).agg(
        {voter: ["count", "nunique"]})
    return (tmp[(voter, "count")] == tmp[(voter, "nunique")]).all()
