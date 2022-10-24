import pandas as pd

from comchoice.aggregate.approval import approval


def pav(
    df,
    delimiter: str = ",",
    n_seats: int = 2,
    ballot: str = "ballot",
    voters: str = "voters"
) -> pd.DataFrame:
    """Proportional Approval Voting

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ",".
    n_seats : int, optional
        Number of seats to fill, by default 2.
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Proportional Approval Voting.
    """
    return approval(
        df,
        delimiter=delimiter,
        method="proportional",
        n_seats=n_seats,
        ballot=ballot,
        voters=voters
    )
