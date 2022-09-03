import pandas as pd
from sqlalchemy import column

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.aggregate.__transform import __transform


def score(
    df,
    aggregation: str = "mean",
    alternative: str = "alternative",
    score: str = "score",
    show_rank: bool = True
) -> pd.DataFrame:
    """Score Voting. (Also called as Range Voting, Utilitarian Voting).

    In this method, voters give a score to each alternative. We average the scores,
    and the winner is the alternative with the highest score.

    Parameters
    ----------
    df : pandas.DataFrame
        A data set to be aggregated.
    aggregation : str, optional
        Aggregation method, by default "mean".
    alternative : str, optional
        Column label that includes the alternatives, by default "alternative".
    score : str, optional
        Column label to be aggregated, by default "score".
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.

    Returns
    -------
    pd.DataFrame
        _description_
    """

    tmp = __aggregate(
        df,
        groupby=[alternative],
        column=score,
        aggregation=aggregation
    )

    tmp = tmp.rename(columns={score: "value"})

    tmp = __set_voters(tmp)
    if show_rank:
        tmp = __set_rank(tmp)

    return tmp
