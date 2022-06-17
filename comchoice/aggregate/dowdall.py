import pandas as pd
from . import borda


def dowdall(
    df,
    candidate="candidate",
    delimiter=">",
    rank="rank",
    rmv=[],
    show_rank=True,
    voters="voters"
) -> pd.DataFrame:
    """Dowdall voting method (1971).

    Dowdall is an alternative to Borda count, devised by Nauru's Secretary
    of Justice in 1971. As in Borda, each voter gives a ranking of candidates.
    The first candidate gets 1 point, the 2nd candidate 1/2 points, and so on
    until the candidate ranked in the n position receives 1/n points.

    Returns
    -------
    pandas.DataFrame:
        a ranking of candidates using Dowdall.

    References
    ----------
    Fraenkel, Jon; Grofman, Bernard (3 April 2014). "The Borda Count and its real-world alternatives: Comparing scoring rules in Nauru and Slovenia". Australian Journal of Political Science. 49 (2): 186-205. doi:10.1080/10361146.2014.900530
    """
    return borda(
        df,
        candidate=candidate,
        delimiter=delimiter,
        rank=rank,
        rmv=rmv,
        score="dowdall",
        show_rank=show_rank,
        voters=voters
    )