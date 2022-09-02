import numpy as np
import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.preprocessing.transform import transform


def judgment(
    df,
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    dtype="ballot",
    method="typical",
    ratings=None,
    show_rank=True,
    transform_kws=transform_kws,
    voters="voters",
    e=0
):
    df = df.copy()

    if voters in list(df):
        df = transform(
            df.copy(),
            **{
                **transform_kws,
                **dict(
                    ballot=ballot,
                    delimiter=delimiter,
                    voters=voters,
                    unique_id=True
                )
            }
        )
    else:
        df[voters] = 1

    ascending = True
    if dtype == "ballot":
        jdgm = []
        for _alternative, tmp in df.groupby("_id"):
            output = []
            for i, items in tmp.iterrows():
                output += [items[ballot]] * items[voters]

            jdgm.append([_alternative, np.median(output)])

        jdgm = pd.DataFrame(jdgm, columns=["_id", "alpha"])
        jdgm = pd.merge(df, jdgm, on="_id")

    elif dtype == "score":
        jdgm = __aggregate(df, groupby=[alternative], aggregation="median", column=ballot)\
            .rename(columns={ballot: "alpha"})
        jdgm = pd.merge(df, jdgm, on=alternative)

        ascending = False

    if dtype == "score" and ratings:
        jdgm[ballot] = jdgm[ballot].replace(ratings)

    jdgm["p" if ascending else "q"] = jdgm[ballot] < np.floor(
        jdgm["alpha"])  # Rate higher than median
    jdgm["q" if ascending else "p"] = jdgm[ballot] > np.floor(
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
