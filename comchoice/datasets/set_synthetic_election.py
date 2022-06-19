from random import choice, sample, seed
from string import ascii_lowercase
import pandas as pd


def set_synthetic_election(
    aggregate=True,
    candidates=None,
    full_rank=True,
    n_candidates=3,
    n_voters=4,
    random_state=None,
    delimiter=">"
) -> pd.DataFrame:
    """Generates synthetic voting data.

    Parameters
    ----------
    candidates: string list, default=alphabet
        List of the names/candidates
    full_rank : bool, default=True
        If the value is `true`, every voter assigns a complete ranking of candidates.
    n_candidates : int, default=3
        Number of candidates. Must be a positive value.
    n_voters : int, default=4
        Number of voters. Must be a positive value.
    random_state : int, None, default=None
        Random state
    rank_separator

    Returns
    -------
    pandas.DataFrame
        A DataFrame of synthetic voting data.

    See Also
    --------
    load_synthetic_pairwise : Generates synthetic voting data.
    """

    if candidates == None:
        if n_candidates <= 26:
            alphabet_string = ascii_lowercase
            candidates = list(alphabet_string[:n_candidates])
        else:
            candidates = list(range(1, n_candidates + 1))
            candidates = [str(c) for c in candidates]
    else:
        n_candidates = len(candidates)

    if random_state != None and (type(random_state) == int or float):
        seed(random_state)

    output = []

    for voter in range(1, n_voters + 1):
        voted = sample(
            candidates, n_candidates) if full_rank else choice(candidates)
        output.append({
            "voters": 1,
            "rank": delimiter.join(voted)
        })

    tmp = pd.DataFrame(output)

    if aggregate:
        tmp = tmp.groupby("rank").agg(
            {"voters": "sum"}).reset_index()
    else:
        tmp = tmp.drop(columns=["voters"])
        tmp["voter"] = range(1, tmp.shape[0] + 1)

    return tmp
