import pandas as pd

from .__aggregate import __aggregate
from .__set_rank import __set_rank
from .__set_voters import __set_voters
from .__transform import __transform


def borda(
    df,
    candidate="candidate",
    delimiter=">",
    rank="rank",
    rmv=[],
    score="original",
    show_rank=True,
    voter="voter",
    voters="voters"
) -> pd.DataFrame:
    """Borda Count (1784).

    The Borda count is a voting method to rank candidates.
    In an election, each voter gives a ranked-ordered list of their preferences.
    Then, it assigns the lowest score to the lowest-ranked candidate, increasing
    the score assigned until the candidate ranks first. The winner is the candidate with the most points.

    The original version proposed by Borda for an election of `n` candidates, assigns `n - 1`
    points to the candidate in the first place, `n - 2` to the candidate in the second place,
    and so on, until assigning 0 to the lowest-ranked candidate.

    Parameters
    ----------
    score: {"original", "score_n", "dowdall"}, default="original"
        Method to calculate Borda score.

    Returns
    -------
    pandas.DataFrame:
        Election results using Borda Count.

    References
    ----------
    Borda, J. D. (1784). Mémoire sur les élections au scrutin. Histoire de l'Academie
    Royale des Sciences pour 1781 (Paris, 1784).
    """

    # if plural_voters:
    df = __transform(df, delimiter=delimiter, rmv=rmv)
    N = len(df[candidate].unique())

    if score == "dowdall":
        df["value"] = 1 / df[rank]

    elif score == "score_n":
        df["value"] = N - df[rank] - 1

    else:
        df["value"] = N - df[rank]

    df = __set_voters(df, voters=voters)
    df = __aggregate(df, groupby=[candidate], aggregation="sum")

    if show_rank:
        df = __set_rank(df)

    return df
