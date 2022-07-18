import numpy as np
import pandas as pd

from comchoice.aggregate.pairwise_matrix import pairwise_matrix
from comchoice.aggregate.__set_rank import __set_rank


def schulze(
    df,
    alternative="alternative",
    rank="rank",
    delimiter=">",
    show_rank=True,
    voter="voter",
    voters="voters"
):

    d = pairwise_matrix(
        df,
        alternative=alternative,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters
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
            if i != j:
                if d[i][j] > d[j][i]:
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
