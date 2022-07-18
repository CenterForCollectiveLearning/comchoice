import pandas as pd

from comchoice.aggregate.approval import approval


def pav(
    df,
    delimiter=",",
    n_seats=2,
    alternatives="alternatives",
    voters="voters"
) -> pd.DataFrame:
    return approval(
        df,
        delimiter=delimiter,
        method="proportional",
        n_seats=n_seats,
        alternatives=alternatives,
        voters=voters
    )
