import pandas as pd


from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.borda import borda
from comchoice.aggregate.condorcet import condorcet


def black(
    df,
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    voter="voter",
    voters="voters",
    transform_kws=transform_kws
) -> pd.DataFrame:
    """Black procedure (1958).

    Calculates winner of an election using Black procedure. First, the method calculates if there is a
    Condorcet winner. If there is a Condorcet winner, that alternative is the winner. Otherwise, the winner
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
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        weak=False,
        transform_kws=transform_kws
    )
    return r if r.shape[0] > 0 else borda(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        score="original",
        show_rank=True,
        voter=voter,
        voters=voters,
        transform_kws=transform_kws
    ).head(1)
