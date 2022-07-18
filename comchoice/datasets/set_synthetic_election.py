from random import choice, sample, seed
from string import ascii_lowercase
import pandas as pd


def set_synthetic_election(
    aggregate=True,
    alternatives=None,
    full_rank=True,
    n_alternatives=3,
    n_voters=4,
    random_state=None,
    delimiter=">"
) -> pd.DataFrame:
    """Generates synthetic voting data.

    Parameters
    ----------
    alternatives: string list, default=alphabet
        List of the names/alternatives
    full_rank : bool, default=True
        If the value is `true`, every voter assigns a complete ranking of alternatives.
    n_alternatives : int, default=3
        Number of alternatives. Must be a positive value.
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

    if alternatives == None:
        if n_alternatives <= 26:
            alphabet_string = ascii_lowercase
            alternatives = list(alphabet_string[:n_alternatives])
        else:
            alternatives = list(range(1, n_alternatives + 1))
            alternatives = [str(c) for c in alternatives]
    else:
        n_alternatives = len(alternatives)

    if random_state != None and (type(random_state) == int or float):
        seed(random_state)

    output = []

    for voter in range(1, n_voters + 1):
        voted = sample(
            alternatives, n_alternatives) if full_rank else choice(alternatives)
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
