import pandas as pd

from comchoice.aggregate.pairwise_matrix import pairwise_matrix
from comchoice.aggregate.__set_rank import __set_rank


def minimax(
    df,
    method="winning_votes",
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

    e = d / (d + d.T)

    if method in ["winning_votes", "pairwise_opposition"]:
        tmp = (1 - e).max(axis=1).to_frame(name="value")
        tmp = tmp.reset_index().rename(columns={"_winner": alternative})
        if method == "winning_votes":
            tmp.loc[tmp["value"] < 0.5, "value"] = 0

    elif method == "margins":
        tmp = (-1 * (e.T - e).min(axis=0)).to_frame(name="value")
        tmp = tmp.reset_index().rename(columns={"_winner": alternative})

    tmp = tmp.sort_values("value", ascending=True)
    tmp = tmp.reset_index(drop=True)

    if show_rank:
        tmp = __set_rank(tmp, ascending=True)

    return tmp
