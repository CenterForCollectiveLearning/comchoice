import pandas as pd


def __set_voters(
    df,
    voters="voters"
):
    if voters in list(df):
        df["value"] *= df[voters]
    return df
