import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.aggregate.__transform import __transform


def borda(
    df,
    alternative="alternative",
    delimiter=">",
    rank="rank",
    rmv=[],
    score="original",
    show_rank=True,
    voter="voter",
    voters="voters",
    **kws
) -> pd.DataFrame:
    """Borda Count (1784).

    The Borda count is a voting method to rank alternatives.
    In an election, each voter gives a ranked-ordered list of their preferences.
    Then, it assigns the lowest score to the lowest-ranked alternative, increasing
    the score assigned until the alternative ranks first. The winner is the alternative with the most points.

    The original version proposed by Borda for an election of `n` alternatives, assigns `n - 1`
    points to the alternative in the first place, `n - 2` to the alternative in the second place,
    and so on, until assigning 0 to the lowest-ranked alternative.

    Parameters
    ----------
    score: {"original", "score_n", "dowdall"}, default="original"
        Method to calculate Borda count.

    Returns
    -------
    pandas.DataFrame:
        Aggregation result using Borda count.

    References
    ----------
    Borda, J. D. (1784). Mémoire sur les élections au scrutin. Histoire de l'Academie
    Royale des Sciences pour 1781 (Paris, 1784).
    """

    # if plural_voters:
    df = __transform(df, delimiter=delimiter, rmv=rmv)
    N = len(df[alternative].unique())

    if score == "dowdall":
        df["value"] = 1 / df[rank]

    elif score == "score_n":
        df["value"] = N - df[rank] - 1

    else:
        df["value"] = N - df[rank]

    df = __set_voters(df, voters=voters)
    df = __aggregate(df, groupby=[alternative], aggregation="sum")

    if show_rank:
        df = __set_rank(df)

    return df
