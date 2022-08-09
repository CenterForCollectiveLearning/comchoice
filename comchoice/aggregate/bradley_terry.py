import numpy as np
import pandas as pd

from comchoice.aggregate.pairwise_matrix import pairwise_matrix
from comchoice.aggregate.__set_rank import __set_rank


def bradley_terry(
    df,
    delimiter=">",
    alternative="alternative",
    ballot="ballot",
    alternative_a="alternative_a",
    alternative_b="alternative_b",
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
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        voter=voter,
        voters=voters
    )

    m = m.values

    ids = set(df[alternative_a]) | set(df[alternative_b])
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
        .rename(columns={"index": alternative}).sort_values("value", ascending=False)

    if show_rank:
        tmp = __set_rank(tmp)

    return tmp
