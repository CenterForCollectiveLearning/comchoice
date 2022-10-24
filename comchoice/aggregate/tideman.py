import numpy as np
import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.pairwise_matrix import pairwise_matrix
from comchoice.aggregate.__set_rank import __set_rank


def tideman(
    df,
    alternative: str = "alternative",
    delimiter: str = ">",
    ballot: str = "ballot",
    show_rank: bool = True,
    voter: str = "voter",
    voters: str = "voters",
    transform_kws: dict = transform_kws
):
    """Tideman.

    Parameters
    ----------
    df : _type_
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.
    voter : str, optional
        _description_, by default "voter"
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".
    transform_kws : dict, optional
        Whether or not to process data.

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Tideman.
    """
    m = pairwise_matrix(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        transform_kws=transform_kws
    )

    m = m - m.T
    m[m < 0] = 0

    tmp = m.sum(axis=0).to_frame(name="value")
    tmp = tmp.reset_index().rename(columns={"_loser": alternative})
    tmp = tmp.reset_index(drop=True)

    if show_rank:
        tmp = __set_rank(tmp, ascending=True)

    return tmp
