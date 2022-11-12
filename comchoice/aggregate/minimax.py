import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.pairwise_matrix import pairwise_matrix


def minimax(
    df: pd.DataFrame,
    method="winning_votes",
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    show_rank=True,
    voter="voter",
    voters="voters",
    transform_kws=transform_kws
) -> pd.DataFrame:
    """Minimax rule.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    method : {"winning_votes", "pairwise_opposition", "margins"}
        Specifies the minimax rule to be used to compute the Minimax algorithm, by default "winning_votes".
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.
    voter : str, optional
        Column label of voter unique identifier, by default "voter".
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Minimax.
    """
    d = pairwise_matrix(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        transform_kws=transform_kws
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
