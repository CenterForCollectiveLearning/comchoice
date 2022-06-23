import pandas as pd

from comchoice.aggregate.approval import approval


def pav(
    df,
    delimiter=",",
    n_seats=2,
    candidates="candidates",
    voters="voters"
) -> pd.DataFrame:
    return approval(
        df,
        delimiter=delimiter,
        method="proportional",
        n_seats=n_seats,
        candidates=candidates,
        voters=voters
    )
