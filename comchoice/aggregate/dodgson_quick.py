import numpy as np
import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.pairwise_matrix import pairwise_matrix


def dodgson_quick(
    df,
    alternative="alternative",
    delimiter=">",
    ballot="ballot",
    show_rank=True,
    voter="voter",
    voters="voters",
    transform_kws=transform_kws
) -> pd.DataFrame:
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

    m = np.ceil(m / 2)

    tmp = m.sum(axis=0).to_frame(name="value")
    tmp = tmp.reset_index().rename(columns={"_loser": alternative})
    tmp = tmp.reset_index(drop=True)

    if show_rank:
        tmp = __set_rank(tmp, ascending=True)

    return tmp
