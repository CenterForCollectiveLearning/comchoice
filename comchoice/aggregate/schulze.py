import numpy as np
import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.pairwise_matrix import pairwise_matrix


def schulze(
    df,
    alternative: str = "alternative",
    ballot: str = "ballot",
    delimiter: str = ">",
    show_rank: bool = True,
    voter: str = "voter",
    voters: str = "voters",
    transform_kws: dict = transform_kws
):
    """Schulze method (2011)

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
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
        Aggregation of preferences using Schulze method.

    References
    ----------
    Schulze, M. (2011). A new monotonic, clone-independent, reversal symmetric, and condorcet-consistent single-winner election method. Social choice and Welfare, 36(2), 267-303.

    """
    d = pairwise_matrix(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        transform_kws=transform_kws
    )

    alternatives = list(d)
    n_alternatives = len(alternatives)

    p = pd.DataFrame(
        np.zeros((n_alternatives, n_alternatives)),
        index=alternatives,
        columns=alternatives
    )

    for i in alternatives:
        for j in alternatives:
            if i != j and d[i][j] > d[j][i]:
                p[i][j] = d[i][j]

    for i in alternatives:
        for j in alternatives:
            if i != j:
                for k in alternatives:
                    if i != k and j != k:
                        p[j][k] = max(p[j][k], min(p[j][i], p[i][k]))

    tmp = pd.DataFrame((p > p.T).astype(int).sum(axis=1)).reset_index()
    tmp.columns = [alternative, "value"]

    if show_rank:
        tmp = tmp.reset_index(drop=True)
        tmp = __set_rank(tmp)

    return tmp
