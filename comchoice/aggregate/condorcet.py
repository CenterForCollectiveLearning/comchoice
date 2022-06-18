import pandas as pd

from . import copeland


def condorcet(
    df,
    candidate="candidate",
    rank="rank",
    delimiter=">",
    voter="voter",
    voters="voters",
    weak=True
):
    """Condorcet winner (1785).

    A Condorcet winner is the candidate who wins 100% of 1v1 elections regarding all
    the other candidates running in the same election (under a plurality rule).

    A weak Condorcet winner does not need to satisfy the rule of 100% of victories.

    Parameters
    ----------
    weak: bool, default=True
        If the value is `true`, returns a weak Condorcet winner.

    Returns
    -------
    pandas.DataFrame:
        Condorcet winner

    References
    ----------
    de Condorcet, M. (1785), Essai sur l'Application de l'Analyse à la Probabilité des Décisions Rendues à la Pluralité des Voix. Paris: L'Imprimerie Royale.

    Felsenthal, D.S., Tideman, N. Weak Condorcet winner(s) revisited. Public Choice 160, 313-326 (2014). https://doi.org/10.1007/s11127-014-0180-4

    """

    tmp = copeland(
        df,
        candidate=candidate,
        rank=rank,
        delimiter=delimiter,
        show_rank=True,
        voter=voter,
        voters=voters
    )

    if weak:
        return tmp.head(1)

    else:
        v = list(tmp["value"].values)
        return pd.DataFrame([]) if v[0] < 1 else tmp.head(1)
