import numpy as np
import pandas as pd

from .pairwise_matrix import pairwise_matrix
from .__set_rank import __set_rank


def tideman(
    df,
    candidate="candidate",
    delimiter=">",
    rank="rank",
    show_rank=True,
    voter="voter",
    voters="voters"
):
    m = pairwise_matrix(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters
    )

    m = m - m.T
    m[m < 0] = 0

    tmp = m.sum(axis=0).to_frame(name="value")
    tmp = tmp.reset_index().rename(columns={"_winner": candidate})
    tmp = tmp.reset_index(drop=True)

    if show_rank:
        tmp = __set_rank(tmp, ascending=True)

    return tmp
