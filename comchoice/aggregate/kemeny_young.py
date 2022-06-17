import pandas as pd
from itertools import combinations, permutations

from . import pairwise_matrix


def kemeny_young(
    df,
    candidate="candidate",
    rank="rank",
    delimiter=">",
    voter="voter",
    voters="voters",
    score_matrix=False
) -> pd.DataFrame:
    """Kemeny-Young method.

    The Kemeny-Young method is a voting method that uses preferential ballots
    and pairwise comparison to identify the most popular candidates in an election.

    Parameters
    ----------
    score_matrix : bool, default = False
        If the value is `true`, returns the score matrix.

    Returns
    -------
    pandas.DataFrame:
        Election results using Kemeny-Young method.

    References
    ----------
    John Kemeny, "Mathematics without numbers", Daedalus 88 (1959), pp. 577-591.

    H. P. Young, "Optimal ranking and choice from pairwise comparisons", in Information pooling and group decision making edited by B. Grofman and G. Owen (1986), JAI Press, pp. 113-122.

    H. P. Young and A. Levenglick, "A Consistent Extension of Condorcet's Election Principle", SIAM Journal on Applied Mathematics 35, no. 2 (1978), pp. 285-300.
    """
    m = pairwise_matrix(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters
    )

    output = []
    for permutation in permutations(list(m)):
        score = 0
        for items in combinations(permutation, 2):
            i_winner, i_loser = items
            value = m.loc[i_winner, i_loser]
            score += value
        output.append([list(permutation), score])

    tmp = pd.DataFrame(output, columns=[rank, "value"]).sort_values(
        "value", ascending=False).reset_index(drop=True)

    if score_matrix:
        return tmp

    tmp_r = pd.DataFrame()
    tmp_r[candidate] = tmp.loc[0, "rank"]
    tmp_r[rank] = range(1, tmp_r.shape[0] + 1)

    return tmp_r
