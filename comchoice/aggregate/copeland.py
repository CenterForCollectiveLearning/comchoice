import numpy as np
import pandas as pd
from comchoice.aggregate.pairwise_matrix import pairwise_matrix

from comchoice.aggregate.__set_rank import __set_rank


def copeland(
    df,
    candidate="candidate",
    rank="rank",
    delimiter=">",
    show_rank=True,
    voter="voter",
    voters="voters"
):
    """Copeland voting method (1951).

    Each voter ranks candidates by preference. Next, we sort candidates by the
    number of times they beat another candidate in a pairwise comparison.
    The top-1 on Copeland's method is considered a weak Condorcet winner.
    Likewise, if in an election of `n` candidates, a candidate beats `n - 1`
    candidates in pairwise comparison scenarios, it is also considered a Condorcet winner.

    Returns
    -------
    pandas.DataFrame:
        Election results using Copeland method.

    References
    ----------
    Copeland, A.H. (1951). A “reasonable” social welfare function, mimeographed. In: Seminar on applications of mathematics to the social sciences. Ann Arbor: Department of Mathematics, University of Michigan.

    """
    m, unique_candidates = pairwise_matrix(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        return_candidates=True
    )

    r = m + m.T
    m = m / r

    m = np.where(m > 0.5, 1, np.where(m == 0.5, 0.5, 0))
    m = pd.DataFrame(m, index=unique_candidates, columns=unique_candidates)
    m = m.reindex(unique_candidates, axis=0)
    m = m.reindex(unique_candidates, axis=1)
    m = m.astype(float)
    np.fill_diagonal(m.values, np.nan)

    tmp = pd.DataFrame([(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=1)))],
                       columns=[candidate, "value"])
    if show_rank:
        tmp = __set_rank(tmp)

    return tmp
