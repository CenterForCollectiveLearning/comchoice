import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.plurality import plurality


def antiplurality(
    df: pd.DataFrame,
    alternative: str = "alternative",
    delimiter: str = ">",
    ballot: str = "ballot",
    show_rank: bool = True,
    voters: str = "voters",
    transform_kws: dict = transform_kws
) -> pd.DataFrame:
    """Antiplurality rule.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".
    transform_kws : dict, optional
        _description_, by default transform_kws

    Returns
    -------
    pd.DataFrame
        _description_
    """
    return plurality(
        df,
        alternative=alternative,
        delimiter=delimiter,
        ballot=ballot,
        show_rank=show_rank,
        voters=voters,
        ascending=True,
        transform_kws=transform_kws
    )
