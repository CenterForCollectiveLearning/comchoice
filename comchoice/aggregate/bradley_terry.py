import numpy as np
import pandas as pd

from . import pairwise_matrix
from .__set_rank import __set_rank


def bradley_terry(
    df,
    delimiter=">",
    candidate="candidate",
    rank="rank",
    candidate_a="candidate_a",
    candidate_b="candidate_b",
    iterations: int = 1,
    show_rank=True,
    voter="voter",
    voters="voters"
) -> pd.DataFrame:
    """Bradley-Terry model (1952)

    Parameters
    ----------
    iterations : int, optional
        _description_, by default 1

    Returns
    -------
    pd.DataFrame
        _description_

    References
    ----------
    Bradley, Ralph Allan; Terry, Milton E. (1952). "Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons". Biometrika. 39 (3/4): 324–345. doi:10.2307/2334029. JSTOR 2334029.
    """

    # self.fit()  # Creates custom columns into the dataset

    m = pairwise_matrix(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters
    )

    m = m.values

    ids = set(df[candidate_a]) | set(df[candidate_b])
    N = len(ids)

    p = np.ones(N)
    pp = np.zeros(N)

    for _ in range(iterations):
        for i in range(N):
            num = 0
            den = 0
            for j in range(N):
                num += m[j, i]
                den += (m[i, j] + m[j, i]) / (p[i] + p[j])

            pp[i] = num / den
        p = pp

    tmp = pd.DataFrame(p / p.sum(), index=ids, columns=["value"]).reset_index()\
        .rename(columns={"index": candidate}).sort_values("value", ascending=False)

    if show_rank:
        tmp = __set_rank(tmp)

    return tmp
