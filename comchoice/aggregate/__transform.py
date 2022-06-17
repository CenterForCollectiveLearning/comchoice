import pandas as pd


def __transform(data, delimiter=">", rmv=[], unique_id=False) -> pd.DataFrame:
    df = data.copy()
    df["_id"] = range(df.shape[0])
    df["rank"] = df["rank"].str.split(delimiter)
    df = df.explode("rank")
    df = df.rename(columns={"rank": "candidate"})

    if len(rmv) > 0:
        df = df[~df["candidate"].isin(rmv)].copy()

    df["rank"] = df.groupby("_id").cumcount() + 1
    if not unique_id:
        df = df.drop(columns=["_id"])

    return df
