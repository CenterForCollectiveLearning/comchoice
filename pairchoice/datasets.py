from itertools import combinations
from os import path
from random import choice, choices, sample
from string import ascii_lowercase
import pandas as pd


def load_chile() -> pd.DataFrame:
    """Loads and returns pairwise comparison data collected in 2019 Chile's revolution.

    Returns
    -------
    data : pandas.DataFrame
        Pairwise comparison data collected in 2019 Chile's revolution.

    References
    ----------
    Navarrete, Carlos; Hidalgo, César, 2022, "Understanding Citizen’s Preferences During Networked Social Movements", [https://doi.org/10.7910/DVN/5JX7CT](https://doi.org/10.7910/DVN/5JX7CT), Harvard Dataverse, V1, UNF:6:KFhOnjjRi0sKsWTqCYgjlQ== [fileUNF]
    """
    __path = path.join(path.dirname(__file__), f"./data/chile_preferences.parquet.gzip")
    return pd.read_parquet(__path)


def load_lebanon() -> pd.DataFrame:
    """Loads and returns pairwise comparison data collected in 2019 Lebanon's revolution.

    Returns
    -------
    data : pandas.DataFrame
        Pairwise comparison data collected in 2019 Lebanon's revolution.

    References
    ----------
    Navarrete, Carlos; Hidalgo, César, 2022, "Understanding Citizen’s Preferences During Networked Social Movements", [https://doi.org/10.7910/DVN/5JX7CT](https://doi.org/10.7910/DVN/5JX7CT), Harvard Dataverse, V1, UNF:6:KFhOnjjRi0sKsWTqCYgjlQ== [fileUNF]
    """
    __path = path.join(path.dirname(__file__), f"./data/lebanon_preferences.parquet.gzip")
    return pd.read_parquet(__path)


def load_synthetic_election(full_rank = True, n_candidates = 3, n_voters = 4) -> pd.DataFrame:
    """Generates synthetic voting data.

    Parameters
    ----------
    full_rank : bool, default=True
        If the value is `true`, every voter assigns a complete ranking of candidates.
    n_candidates : int, default=3
        Number of candidates. Must be a positive value.
    n_voters : int, default=4
        Number of voters. Must be a positive value.
        
    Returns
    -------
    pandas.DataFrame
        A DataFrame of synthetic voting data.

    See Also
    --------
    load_synthetic_pairwise : Generates synthetic voting data.
    """
    alphabet_string = ascii_lowercase
    candidates = list(alphabet_string[:n_candidates])

    output = []

    for voter in range(1, n_voters + 1):
        voted = sample(candidates, n_candidates) if full_rank else choice(candidates)
        output.append({
            "voters": 1,
            "rank": "".join(voted)
        })

    tmp = pd.DataFrame(output).groupby("rank").agg({"voters": "sum"}).reset_index()
    tmp["rank"] = tmp["rank"].apply(lambda x: list(x))

    return tmp


def load_synthetic_pairwise(
    n_candidates = 3, 
    n_voters = 10, 
    ties = False, 
    transitive = True, 
    weight_tie = 0.1
) -> pd.DataFrame:
    """Generates synthetic pairwise comparison data.
    
    Parameters
    ----------
    n_candidates : int, default=3
        Number of candidates. Must be a positive value.
    n_voters : int, default=10
        Number of voters. Must be a positive value.
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

    candidates = list(range(1, n_candidates + 1))
    voters = list(range(1, n_voters + 1))

    output = []

    for voter in voters:
        rank_order = combinations(sample(candidates, n_candidates), 2)
        for candidate_a, candidate_b in rank_order:

            options = sample([candidate_a, candidate_b], 2)
            option_a = options[0]
            option_b = options[1]

            selected = choices([candidate_a, 0], weights = [1 - weight_tie, weight_tie])[0] if ties else candidate_a

            output.append({
                "voter": voter,
                "option_a": option_a,
                "option_b": option_b,
                "selected": selected
            })

    return pd.DataFrame(output)