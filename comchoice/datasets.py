from itertools import combinations
from os import path
from random import choice, choices, sample, seed
from string import ascii_lowercase
import pandas as pd
import re
import urllib


def from_preflib(path):
    """
    Converts Preflib Data
    """
    file = urllib.request.urlopen(path)
    arr = file.read().decode('utf-8').split("\n")
    _ = path.split(".")[-1]

    output = []
    nodes = int(arr[0])
    for index, line in enumerate(arr):
        output.append(line.split(",", 1))

    df = pd.DataFrame(output).dropna()

    df_nodes = df.head(nodes).copy()
    df_nodes = df_nodes.rename(columns={0: "node_id", 1: "node_name"})
    df_edges = df[nodes+1:df.shape[0]].copy()

    if _ in ["toc"]:
        cols = ["winners", "losers"]
        df_edges[cols] = df_edges.apply(
            lambda x: [item for item in re.split(r",\{(.*?)\}", x[1])[:2]],
            axis=1,
            result_type="expand"
        )
        for col in cols:
            df_edges[col] = df_edges[col].str.replace(
                "{", "", regex=False).str.replace("}", "", regex=False)

    elif _ in ["soc"]:
        df_edges = df_edges.rename(columns={1: "rank"})

    else:
        cols = ["source", "destination"]
        df_edges[cols] = df_edges[1].str.split(",", expand=True)

    df_edges = df_edges.rename(columns={0: "voters"})
    df_edges = df_edges.drop(columns=[1], errors="ignore")

    return df_nodes, df_edges


def load_synthetic_election(
    candidates=None,
    full_rank=True,
    n_candidates=3,
    n_voters=4,
    random_state=None,
    rank_separator=">"
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

    if candidates == None or len(candidates) != n_candidates:
        if n_candidates <= 26:
            alphabet_string = ascii_lowercase
            candidates = list(alphabet_string[:n_candidates])
        else:
            candidates = list(range(1, n_candidates + 1))
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
            "rank": rank_separator.join(voted)
        })

    tmp = pd.DataFrame(output).groupby("rank").agg(
        {"voters": "sum"}).reset_index()

    return tmp


def load_synthetic_pairwise(
    n_candidates=3,
    n_voters=10,
    random_state=None,
    ties=False,
    transitive=True,
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
