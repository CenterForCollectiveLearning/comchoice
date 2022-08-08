import pandas as pd


def __transform(
    data,
    delimiter=">",
    ballot="rank",
    rmv=[],
    unique_id=False,
    **kws
) -> pd.DataFrame:
    df = data.copy()
    df["_id"] = range(df.shape[0])

    if ballot == "rank":
        df["rank"] = df["rank"].str.split(delimiter)
        df = df.explode("rank")
        df = df.rename(columns={"rank": "alternative"})

        if len(rmv) > 0:
            df = df[~df["alternative"].isin(rmv)].copy()

        df["rank"] = df.groupby("_id").cumcount() + 1

    elif ballot == "score":
        df["alternative"] = df["ballot"].str.split(",")
        df = df.explode("alternative")
        df[["alternative", "score"]] = df["alternative"].str.split(
            "=", n=1, expand=True)
        df["score"] = df["score"].astype(float)
        df = df.drop(columns=["ballot"])

    if not unique_id:
        df = df.drop(columns=["_id"])

    return df
