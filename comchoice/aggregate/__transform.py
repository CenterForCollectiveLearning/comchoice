import pandas as pd


from comchoice.preprocessing.to_pairwise import to_pairwise as to_pw


def __transform(
    data,
    ballot="rank",
    delimiter=">",
    rmv=[],
    score_delimiter="=",
    to_pairwise=False,
    unique_id=False,
    **kws
) -> pd.DataFrame:
    """Transforms a DataFrame into a machine-friendly DataFrame.

    Parameters
    ----------
    data : pd.DataFrame
        A pandas DataFrame.
    delimiter : str, optional
        Whether alternatives are separated in the column, by default ">"
    ballot : {"rank", "score"}, optional
        DataFrame format. Values accepted are "rank" and "score", by default "rank"
    rmv : list, optional
        Remove alternatives from list, before calculating ranking, by default []
    score_delimiter : str, optional
        In case of ballot = "score", defines how alternative and score are separated, by default "="
    unique_id : bool, optional
        Returns internal unique_id generated in the function to convert the DataFrame, by default False

    Returns
    -------
    pd.DataFrame
        A transformed DataFrame.
    """
    df = data.copy()
    df["_id"] = range(df.shape[0])

    if ballot == "rank":
        df["rank"] = df["rank"].str.split(delimiter)
        df = df.explode("rank")
        df = df.rename(columns={"rank": "alternative"})

        if len(rmv) > 0:
            df = df[~df["alternative"].isin(rmv)].copy()

        # TODO: Allow ties in ballots.
        df["rank"] = df.groupby("_id").cumcount() + 1

    elif ballot == "score":
        df["alternative"] = df["ballot"].str.split(delimiter)
        df = df.explode("alternative")
        df[["alternative", "score"]] = df["alternative"].str.split(
            score_delimiter, n=1, expand=True)
        df["score"] = df["score"].astype(float)
        df = df.drop(columns=["ballot"])

    if to_pairwise:
        df = to_pw(
            voter="_id"
        )

    if not unique_id:
        df = df.drop(columns=["_id"])

    return df
