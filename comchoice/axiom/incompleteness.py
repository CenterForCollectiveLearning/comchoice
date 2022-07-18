import pandas as pd

from comchoice.axiom.completeness import completeness


def incompleteness(
    df,
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    n_alternatives=2,
    n_preferences=2,
    voter="voter"
) -> bool:
    """
    Incompleteness: a data is incomplete if any alternative does not provided their
    entire pairwise preferences between all the alternatives.

    Returns
    -------
    bool: 
        Boolean variable to indicate if the data is complete.
    """
    return not completeness(
        df,
        alternative_a=alternative_a,
        alternative_b=alternative_b,
        n_alternatives=n_alternatives,
        n_preferences=n_preferences,
        voter=voter
    )
