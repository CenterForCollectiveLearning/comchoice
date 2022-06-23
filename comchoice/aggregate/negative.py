import pandas as pd

from comchoice.aggregate.score import score


def negative(
    df,
    candidate="candidate",
    score="score",
    show_rank=True
) -> pd.DataFrame:
    """Negative Voting.

    Calculates the score of each candidate using Negative Voting.

    Returns
    -------
    pandas.DataFrame: 
        Election results using Negative Voting.

    """
    return score(
        df,
        aggregation="sum",
        candidate=candidate,
        score=score,
        show_rank=show_rank
    )
