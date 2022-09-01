import pandas as pd


def score_extend(
    df,
    delimiter=";",
    ballot="ballot",
    delimiter_score="=",
    unique_id=False,
    ascending=False
):
    df["_id"] = range(df.shape[0])

    df["alternative"] = df[ballot].str.split(delimiter)
    df = df.explode("alternative")

    df[["alternative", ballot]] = df["alternative"].str.split(
        delimiter_score, n=1, expand=True)

    df[ballot] = df[ballot].astype(float)
    if (df[ballot] % 1 == 0).all():
        df[ballot] = df[ballot].astype(int)

    df["rank"] = df.groupby("_id")[ballot].rank(
        method="min", ascending=ascending).astype(int)

    if not unique_id:
        df = df.drop(columns=["_id"])

    return df
