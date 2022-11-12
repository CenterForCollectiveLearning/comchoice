import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.preprocessing.transform import transform


def k_approval(
    df: pd.DataFrame,
    k: int = 2,
    alternative: str = "alternative",
    ballot: str = "ballot",
    delimiter: str = ">",
    show_rank: bool = True,
    voters: str = "voters",
    transform_kws: dict = transform_kws,
) -> pd.DataFrame:
    """k-Approval method.

    The method gives 1 if the alternative is ranked over or equal to k. Otherwise, the value given is 0.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    k : int, optional
        Rank threshold to score alternatives, by default 2. When `k = 2`, it is the equivalent of Plurality rule.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".
    transform_kws : dict, optional
        Whether or not to process data.

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using k-Approval.
    """
    df = transform(
        df.copy(),
        ballot=ballot,
        delimiter=delimiter,
        voters=voters,
        **transform_kws
    )
    df["value"] = df[ballot] <= k

    df = __set_voters(df, voters=voters)
    df = __aggregate(df, groupby=[alternative], aggregation="sum")

    if show_rank:
        df = __set_rank(df)

    return df
