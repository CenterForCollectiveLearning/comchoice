import pandas as pd

from comchoice.aggregate.score import score


def cumulative(
    df,
    alternative: str = "alternative",
    score: str = "score",
    show_rank: bool = True
) -> pd.DataFrame:
    """Cumulative Voting.

    Calculates the cumulative score of each alternative.

    Returns
    -------
    pandas.DataFrame:
        Election results using Cumulative Voting
    """
    return score(
        df,
        aggregation="sum",
        alternative=alternative,
        score=score,
        show_rank=show_rank
    )
