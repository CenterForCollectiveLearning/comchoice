import numpy as np
import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.preprocessing.transform import transform


def judgment(
    df,
    alternative: str = "alternative",
    ballot: str = "ballot",
    delimiter: str = ">",
    dtype: str = "ballot",
    method: str = "typical",
    ratings=None,
    show_rank: bool = True,
    transform_kws: dict = transform_kws,
    voters: str = "voters",
    e: int = 0
):
    """Judgment rule. These family of rules relies on the median score in order to elect a winner.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    dtype : str, optional
        _description_, by default "ballot"
    method : {"typical", "usual", "central", "bucklin", "majority"}
        Judgment method to use in case of a tie, by default "typical".
    ratings : _type_, optional
        _description_, by default None
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.
    transform_kws : dict, optional
        Whether or not to process data.
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".
    e : int, optional
        Error variable used when `method = "central"`, by default 0.

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using a highest-majority rule.

    References
    ----------
    Lang, J., & Slavkovik, M. (2013, November). Judgment aggregation rules and voting rules. In International Conference on Algorithmic Decision Theory (pp. 230-243). Springer, Berlin, Heidelberg.

    """
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
                output += [items["rank"]] * items[voters]

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

    jdgm["p" if ascending else "q"] = jdgm["rank"] < np.floor(
        jdgm["alpha"])  # Rate higher than median
    jdgm["q" if ascending else "p"] = jdgm["rank"] > np.floor(
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
