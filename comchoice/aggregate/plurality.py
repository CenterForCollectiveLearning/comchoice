import pandas as pd

from comchoice.aggregate.__aggregate import __aggregate
from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_voters import __set_voters
from comchoice.preprocessing.transform import transform


def plurality(
    df,
    alternative: str = "alternative",
    delimiter: str = ">",
    ballot: str = "ballot",
    show_rank: bool = True,
    voters: str = "voters",
    ascending: bool = False,
    transform_kws: dict = transform_kws
) -> pd.DataFrame:
    """Plurality Rule.

    Each voter selects one alternative (or none if voters can abstain), and the alternative(s) with the most votes win.

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
    ascending : bool, optional
        Whether the score is sorted ascending or not, by default False. When `ascending = True`, the method is called Anti-Plurality.

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Plurality rule.
    """

    df = transform(
        df.copy(),
        **{
            **transform_kws,
            **dict(
                ballot=ballot,
                delimiter=delimiter,
                voters=voters,
            )
        }
    )

    df = df[df["rank"] == 1].copy()
    df["value"] = 1
    df = __set_voters(df, voters=voters)
    alternatives = df[alternative].unique()
    tmp = df.groupby(alternative).agg({"value": "sum"})\
        .reindex(alternatives).fillna(0)\
        .reset_index()

    if show_rank:
        tmp = __set_rank(tmp, ascending=ascending)

    return tmp
