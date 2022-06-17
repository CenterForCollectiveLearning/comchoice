import pandas as pd


def __set_rank(df, ascending=False) -> pd.DataFrame:
    df["rank"] = df["value"].rank(
        method="min", ascending=ascending).astype(int)

    df = df.sort_values("rank")
    return df
