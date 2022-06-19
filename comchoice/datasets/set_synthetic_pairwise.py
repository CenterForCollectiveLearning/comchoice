from itertools import combinations
from random import choices, sample, seed
from string import ascii_lowercase
import pandas as pd


def set_synthetic_pairwise(
    n_candidates=3,
    n_voters=10,
    random_state=None,
    ties=False,
    weight_tie=0.1,
    candidates=None
) -> pd.DataFrame:
    """Generates synthetic pairwise comparison data.

    Parameters
    ----------
    candidates: string list, default=numbers
        List of the names/candidates
    n_candidates : int, default=3
        Number of candidates. Must be a positive value.
    n_voters : int, default=10
        Number of voters. Must be a positive value.
    random_state : int, None, default=None
        Random state
    ties : bool, default=False
        If the value is `true`, the data will include ties between comparisons.
    transitive : bool, default=True
        If the value is `true`, individual preferences are transitives.
    weight_tie : float, default=0.1
        Probability of a tie in a pairwise choice. It works if ties=True.

    Returns
    -------
    pandas.DataFrame
        A DataFrame of synthetic pairwise comparison data.

    See Also
    --------
    load_synthetic_election : Generates synthetic voting data.
    """
    if candidates == None:
        candidates = list(range(1, n_candidates + 1))
    else:
        n_candidates = len(candidates)

    if random_state != None and (type(random_state) == int or float):
        seed(random_state)

    voters = list(range(1, n_voters + 1))

    output = []

    for voter in voters:
        rank_order = combinations(sample(candidates, n_candidates), 2)
        for candidate_a, candidate_b in rank_order:

            options = sample([candidate_a, candidate_b], 2)
            option_a = options[0]
            option_b = options[1]

            selected = choices([candidate_a, 0], weights=[
                               1 - weight_tie, weight_tie])[0] if ties else candidate_a

            output.append({
                "voter": voter,
                "option_a": option_a,
                "option_b": option_b,
                "selected": selected
            })

    return pd.DataFrame(output)
