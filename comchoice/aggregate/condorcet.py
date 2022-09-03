import pandas as pd

from comchoice.aggregate.copeland import copeland
from comchoice.aggregate.__default_parameters import transform_kws


def condorcet(
    df,
    alternative: str = "alternative",
    ballot: str = "ballot",
    delimiter: str = ">",
    voter: str = "voter",
    voters: str = "voters",
    weak: bool = True,
    transform_kws: dict = transform_kws
):
    """Condorcet winner (1785).

    A Condorcet winner is the alternative who wins 100% of 1v1 elections regarding all
    the other alternatives running in the same election (under a plurality rule).

    A weak Condorcet winner does not need to satisfy the rule of 100% of victories.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    ballot : str, optional
       Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    delimiter : str, optional
       Delimiter used between alternatives in a `ballot`, by default ">".
    voter : str, optional
        Column label of voter unique identifier, by default "voter".
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".
    weak : bool, optional
        Whether or not returns a weak Condorcet winner, by default True.

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
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        show_rank=True,
        voter=voter,
        voters=voters,
        transform_kws=transform_kws
    )

    if weak:
        return tmp.head(1)

    else:
        v = list(tmp["value"].values)
        return pd.DataFrame([]) if v[0] < 1 else tmp.head(1)
