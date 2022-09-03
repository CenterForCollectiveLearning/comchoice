import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.preprocessing.transform import transform


def borda(
    df,
    alternative: str = "alternative",
    delimiter: str = ">",
    ballot: str = "ballot",
    score: str = "original",
    show_rank: bool = True,
    voters: str = "voters",
    transform_kws: dict = transform_kws,
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
    df : _type_
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    rmv : list, optional
        List of alternatives to exclude before computing the score by the rule, by default [].
    score : {"original", "score_n", "dowdall"}
        Specifies the minimax rule to be used to compute Borda, by default "original".
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.
    transform_kws: dict, optional
        Whether or not to process data.
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Borda count.

    References
    ----------
    Borda, J. D. (1784). Mémoire sur les élections au scrutin. Histoire de l'Academie
    Royale des Sciences pour 1781 (Paris, 1784).
    """
    df = transform(
        df.copy(),
        ballot=ballot,
        delimiter=delimiter,
        voters=voters,
        **transform_kws
    )
    N = len(df[alternative].unique())

    if score == "dowdall":
        df["value"] = 1 / df[ballot]

    elif score == "score_n":
        df["value"] = N - df[ballot] - 1

    else:
        df["value"] = N - df[ballot]

    df = __set_voters(df, voters=voters)
    df = __aggregate(df, groupby=[alternative], aggregation="sum")

    if show_rank:
        df = __set_rank(df)

    return df
