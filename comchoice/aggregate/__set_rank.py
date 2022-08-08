import pandas as pd


def __set_rank(
    df,
    column="value",
    method="min",
    ascending=False
) -> pd.DataFrame:
    """Computes a rank column from alternatives' scores.

    Parameters
    ----------
    df : pandas.DataFrame
        A pandas DataFrame.
    column : str, optional
        Column name in which we want to compute the rank, by default "value"
    method : str, optional
        A pandas.rank method to define how to compute the ranking in case of ties, by default "min"
    ascending : bool, optional
        A pandas.rank method to define whether or not the alternatives should be ranked in ascending order, by default False

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame including a new column called rank.
    """
    df["rank"] = df[column].rank(
        method=method,
        ascending=ascending
    ).astype(int)

    df = df.sort_values("rank")

    return df
