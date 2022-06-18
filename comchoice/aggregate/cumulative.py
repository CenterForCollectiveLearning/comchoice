import pandas as pd

from . import score


def cumulative(
    df,
    candidate="candidate",
    score="score",
    show_rank=True
) -> pd.DataFrame:
    """Cumulative Voting.

    Calculates the cumulative score of each candidate.

    Returns
    -------
    pandas.DataFrame:
        Election results using Cumulative Voting
    """
    return score(
        df,
        aggregation="sum",
        candidate=candidate,
        score=score,
        show_rank=show_rank
    )
