import pandas as pd
from math import factorial


def __combinations_for_completeness(
    n_alternatives=2,
    n_preferences=2
):
    num = factorial(n_alternatives)
    den = factorial(n_preferences) * factorial(n_alternatives - n_preferences)
    return num / den


def completeness(
    df,
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    n_alternatives=2,
    n_preferences=2,
    voter="voter"
) -> bool:
    """
    Completeness: a data is complete if all alternatives provided their
    pairwise preferences between all the alternatives.

    Returns
    -------
    bool:
        Boolean variable to indicate if the data is complete.
    """
    columns = [alternative_a, alternative_b, voter]
    min_num = df.drop_duplicates(subset=columns)\
        .groupby(voter)[alternative_a].count().min()

    expected_num = __combinations_for_completeness(
        n_alternatives=n_alternatives,
        n_preferences=n_preferences
    )

    return min_num == expected_num
