import pandas as pd


from . import borda, condorcet


def black(
    df,
    candidate="candidate",
    rank="rank",
    delimiter=">",
    voter="voter",
    voters="voters"
) -> pd.DataFrame:
    """Black procedure (1958).

    Calculates winner of an election using Black procedure. First, the method calculates if there is a
    Condorcet winner. If there is a Condorcet winner, that candidate is the winner. Otherwise, the winner
    using Borda count is the winner.

    Returns
    -------
    pandas.DataFrame:
        Election's winner using Black procedure.

    References
    ----------
    Black, Duncan (1958). The theory of committees and elections. Cambridge: University Press.
    """
    r = condorcet(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        weak=False
    )
    return r if r.shape[0] > 0 else borda(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        score="original",
        show_rank=True,
        voter=voter,
        voters=voters,
        weak=False
    ).head(1)
