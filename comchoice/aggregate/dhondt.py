import pandas as pd


def dhondt(
    df,
    party="party",
    votes="votes",
    seats=1
) -> pd.DataFrame:
    """D'Hondt (or Jefferson) method.

    Calculates the number of elected candidates of each party using the D'Hondt (or Jefferson) method.

    Parameters
    ----------
    seats : int, default=1, optional:
        Number of seats to be assigned in the election.

    Returns
    -------
    pandas.DataFrame:
        Summary with the seats of each party.
    """
    output = []
    for __party, df_tmp in df.groupby(party):
        votes = df_tmp["votes"].values[0]
        for i in range(seats):
            output.append({party: __party, "quot": votes / (i + 1)})

    tmp = pd.DataFrame(output).sort_values("quot", ascending=False)
    return tmp.head(seats).groupby(party).count().reset_index().rename(columns={"quot": "seats"})
