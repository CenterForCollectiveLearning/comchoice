import pandas as pd

from comchoice.axiom.completeness import completeness


def incompleteness(
    df,
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    n_candidates=2,
    n_preferences=2,
    voter="voter"
) -> bool:
    """
    Incompleteness: a data is incomplete if any candidate does not provided their
    entire pairwise preferences between all the candidates.

    Returns
    -------
    bool: 
        Boolean variable to indicate if the data is complete.
    """
    return not completeness(
        df,
        alternative_a=alternative_a,
        alternative_b=alternative_b,
        n_candidates=n_candidates,
        n_preferences=n_preferences,
        voter=voter
    )
