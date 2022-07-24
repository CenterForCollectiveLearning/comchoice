import numpy as np
import pandas as pd
from comchoice.aggregate.pairwise_matrix import pairwise_matrix

from comchoice.aggregate.__set_rank import __set_rank


def copeland(
    df,
    alternative="alternative",
    delimiter=">",
    pairwise_matrix=False,
    rank="rank",
    show_rank=True,
    voter="voter",
    voters="voters"
):
    """Copeland voting method (1951).

    Each voter ranks alternatives by preference. Next, we sort alternatives by the
    number of times they beat another alternative in a pairwise comparison.
    The top-1 on Copeland's method is considered a weak Condorcet winner.
    Likewise, if in an election of `n` alternatives, a alternative beats `n - 1`
    alternatives in pairwise comparison scenarios, it is also considered a Condorcet winner.

    Returns
    -------
    pandas.DataFrame:
        Election results using Copeland method.

    References
    ----------
    Copeland, A.H. (1951). A “reasonable” social welfare function, mimeographed. In: Seminar on applications of mathematics to the social sciences. Ann Arbor: Department of Mathematics, University of Michigan.

    """

    if pairwise_matrix:
        m = df
        unique_alternatives = list(df)

    else:
        m, unique_alternatives = pairwise_matrix(
            df,
            alternative=alternative,
            rank=rank,
            delimiter=delimiter,
            voter=voter,
            voters=voters,
            return_alternatives=True
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
