import pandas as pd


def ballot_extend(
    df,
    ballot="ballot",
    delimiter=">",
    delimiter_ties="=",
    rmv=[],
    unique_id=False
):
    df["voter"] = range(df.shape[0])
    df[ballot] = df[ballot].str.split(delimiter)
    df = df.explode(ballot)

    df = df.rename(columns={ballot: "alternative"})
    if len(rmv) > 0:
        df = df[~df["alternative"].isin(rmv)].copy()

    df["rank_a"] = df.groupby("voter").cumcount() + 1

    df["alternative"] = df["alternative"].str.split(delimiter_ties)
    df["rank_b"] = df["alternative"].map(len)
    df["rank_b"] = df.groupby("voter")["rank_b"].cumsum()

    df["rank"] = df.apply(lambda x: x["rank_a"] if len(
        x["alternative"]) > 1 else x["rank_b"], axis=1)
    df = df.explode("alternative")

    df = df.drop(columns=["rank_a", "rank_b"])

    if not unique_id:
        df = df.drop(columns=["voter"])

    return df
