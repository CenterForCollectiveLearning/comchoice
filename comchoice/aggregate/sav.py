import pandas as pd

from comchoice.aggregate.approval import approval


def sav(
    df,
    delimiter: str = ",",
    n_seats: int = 2,
    ballot: str = "ballot",
    voters: str = "voters"
) -> pd.DataFrame:
    return approval(
        df,
        delimiter=delimiter,
        method="satisfaction",
        n_seats=n_seats,
        ballot=ballot,
        voters=voters
    )
