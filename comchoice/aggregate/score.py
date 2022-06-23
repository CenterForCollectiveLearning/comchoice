import pandas as pd
from sqlalchemy import column

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.aggregate.__transform import __transform


def score(
    df,
    aggregation="mean",
    candidate="candidate",
    score="score",
    show_rank=True
) -> pd.DataFrame:
    """Score Voting. (Also called as Range Voting, Utilitarian Voting).

    In this method, voters give a score to each candidate. We average the scores,
    and the winner is the candidate with the highest score.

    Returns
    -------
    pandas.DataFrame:
        Election results using Score Voting.

    """
    tmp = __aggregate(
        df,
        groupby=[candidate],
        column=score,
        aggregation=aggregation
    )

    tmp = tmp.rename(columns={score: "value"})

    tmp = __set_voters(tmp)
    if show_rank:
        tmp = __set_rank(tmp)

    return tmp
