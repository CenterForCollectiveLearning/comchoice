import numpy as np
import pandas as pd

from comchoice.aggregate.pairwise_matrix import pairwise_matrix
from comchoice.aggregate.__set_rank import __set_rank


def schulze(
    df,
    candidate="candidate",
    rank="rank",
    delimiter=">",
    show_rank=True,
    voter="voter",
    voters="voters"
):

    d = pairwise_matrix(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters
    )

    candidates = list(d)
    n_candidates = len(candidates)

    p = pd.DataFrame(
        np.zeros((n_candidates, n_candidates)),
        index=candidates,
        columns=candidates
    )

    for i in candidates:
        for j in candidates:
            if i != j:
                if d[i][j] > d[j][i]:
                    p[i][j] = d[i][j]

    for i in candidates:
        for j in candidates:
            if i != j:
                for k in candidates:
                    if i != k and j != k:
                        p[j][k] = max(p[j][k], min(p[j][i], p[i][k]))

    tmp = pd.DataFrame((p > p.T).astype(int).sum(axis=1)).reset_index()
    tmp.columns = [candidate, "value"]

    if show_rank:
        tmp = tmp.reset_index(drop=True)
        tmp = __set_rank(tmp)

    return tmp
