import pandas as pd

from .pairwise_matrix import pairwise_matrix


def minimax(
    df,
    method="winning_votes",
    candidate="candidate",
    rank="rank",
    delimiter=">",
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

    e = d / (d + d.T)

    if method in ["winning_votes", "pairwise_opposition"]:
        tmp = (1 - e).max(axis=1).to_frame(name="value")
        tmp = tmp.reset_index().rename(columns={"_winner": candidate})
        if method == "winning_votes":
            tmp.loc[tmp["value"] < 0.5, "value"] = 0

    elif method == "margins":
        tmp = (-1 * (e.T - e).min(axis=0)).to_frame(name="value")
        tmp = tmp.reset_index().rename(columns={"_winner": candidate})

    tmp = tmp.sort_values("value", ascending=True)
    tmp = tmp.reset_index(drop=True)

    return tmp
