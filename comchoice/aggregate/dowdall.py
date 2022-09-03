import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.borda import borda


def dowdall(
    df,
    alternative: str = "alternative",
    delimiter: str = ">",
    ballot: str = "ballot",
    show_rank: bool = True,
    voters: str = "voters",
    transform_kws: dict = transform_kws
) -> pd.DataFrame:
    """Dowdall voting method (1971).

    Dowdall is an alternative to Borda count, devised by Nauru's Secretary
    of Justice in 1971. As in Borda, each voter gives a ranking of alternatives.
    The first alternative gets 1 point, the 2nd alternative 1/2 points, and so on
    until the alternative ranked in the n position receives 1/n points.

    Parameters
    ----------
    df : _type_
        _description_
    alternative : str, optional
        _description_, by default "alternative"
    delimiter : str, optional
        _description_, by default ">"
    ballot : str, optional
        _description_, by default "ballot"
    show_rank : bool, optional
        _description_, by default True
    voters : str, optional
        _description_, by default "voters"
    transform_kws : dict, optional
        _description_, by default transform_kws

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Dowdall.

    References
    ----------
    Fraenkel, Jon; Grofman, Bernard (3 April 2014). "The Borda Count and its real-world alternatives: Comparing scoring rules in Nauru and Slovenia". Australian Journal of Political Science. 49 (2): 186-205. doi:10.1080/10361146.2014.900530
    """
    return borda(
        df,
        alternative=alternative,
        delimiter=delimiter,
        ballot=ballot,
        score="dowdall",
        show_rank=show_rank,
        voters=voters,
        transform_kws=transform_kws
    )
