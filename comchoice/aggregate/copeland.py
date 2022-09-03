import numpy as np
import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.pairwise_matrix import pairwise_matrix


def copeland(
    df,
    alternative="alternative",
    delimiter=">",
    pw_matrix=False,
    ballot="ballot",
    show_rank=True,
    voter="voter",
    voters="voters",
    transform_kws=transform_kws
):
    """Copeland voting method (1951).

    Each voter ranks alternatives by preference. Next, we sort alternatives by the
    number of times they beat another alternative in a pairwise comparison.
    The top-1 on Copeland's method is always a weak Condorcet winner.
    Likewise, if in an election of `n` alternatives, a alternative beats `n - 1`
    alternatives in pairwise comparison scenarios, it is also considered a Condorcet winner.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    pw_matrix : bool, optional
        A Pairwise Matrix is set in df, by default False.
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.
    voter : str, optional
        Column label of voter unique identifier, by default "voter".
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Copeland.

    References
    ----------
    Copeland, A.H. (1951). A “reasonable” social welfare function, mimeographed. In: Seminar on applications of mathematics to the social sciences. Ann Arbor: Department of Mathematics, University of Michigan.
    """

    if pw_matrix:
        m = df
        unique_alternatives = list(df)

    else:
        m, unique_alternatives = pairwise_matrix(
            df,
            alternative=alternative,
            ballot=ballot,
            delimiter=delimiter,
            voter=voter,
            voters=voters,
            return_alternatives=True,
            transform_kws=transform_kws
        )

    r = m + m.T
    m = m / r

    m = np.where(m > 0.5, 1, np.where(m == 0.5, 0.5, 0))
    m = pd.DataFrame(m, index=unique_alternatives, columns=unique_alternatives)
    m = m.reindex(unique_alternatives, axis=0)
    m = m.reindex(unique_alternatives, axis=1)
    m = m.astype(float)
    np.fill_diagonal(m.values, np.nan)

    tmp = pd.DataFrame([(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=1)))],
                       columns=[alternative, "value"])
    if show_rank:
        tmp = __set_rank(tmp)

    return tmp
