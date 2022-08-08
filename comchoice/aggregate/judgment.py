import numpy as np
import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.aggregate.__transform import __transform


def judgment(
    df,
    alternative="alternative",
    column="rank",
    delimiter=">",
    method="typical",
    ratings=None,
    show_rank=True,
    source="rank",
    transform_kws=dict(ballot="rank"),
    voter="voter",
    voters="voters",
    e=0
):
    if voters in list(df):
        df = __transform(
            df,
            delimiter=delimiter,
            unique_id=True,
            **transform_kws
        )
    else:
        df[voters] = 1

    ascending = True
    if source == "rank":
        jdgm = []
        for _alternative, tmp in df.groupby("_id"):
            output = []
            for i, items in tmp.iterrows():
                output += [items[column]] * items[voters]

            jdgm.append([_alternative, np.median(output)])

        jdgm = pd.DataFrame(jdgm, columns=["_id", "alpha"])
        jdgm = pd.merge(df, jdgm, on="_id")

    elif source == "score":
        jdgm = __aggregate(df, groupby=[alternative], aggregation="median", column=column)\
            .rename(columns={column: "alpha"})
        jdgm = pd.merge(df, jdgm, on=alternative)

        ascending = False

    if column == "score" and ratings:
        jdgm[column] = jdgm[column].replace(ratings)

    jdgm["p" if ascending else "q"] = jdgm[column] < np.floor(
        jdgm["alpha"])  # Rate higher than median
    jdgm["q" if ascending else "p"] = jdgm[column] > np.floor(
        jdgm["alpha"])  # Rate lower than median

    for col in ["p", "q"]:
        jdgm[col] = jdgm[col].astype(int)

    jdgm = jdgm.groupby(alternative).agg(
        {"alpha": "mean", "p": "mean", "q": "mean"}).reset_index()

    if method == "typical":
        jdgm["value"] = jdgm["alpha"] + jdgm["p"] - jdgm["q"]

    elif method == "usual":
        jdgm["value"] = jdgm["alpha"] + 0.5 * \
            (jdgm["p"] - jdgm["q"]) / (1 - jdgm["p"] - jdgm["q"])

    elif method == "central":
        jdgm["value"] = jdgm["alpha"] + 0.5 * \
            (jdgm["p"] - jdgm["q"]) / (jdgm["p"] + jdgm["q"] + e)

    elif method == "bucklin":
        jdgm["value"] = jdgm["alpha"] - jdgm["q"]

    elif method == "majority":
        jdgm["value"] = jdgm.apply(lambda x: x["p"] if (
            x["p"] > x["q"]) else -x["q"], axis=1)

    if show_rank:
        jdgm = __set_rank(jdgm, ascending=False)

    return jdgm
