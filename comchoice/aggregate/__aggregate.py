import pandas as pd


def __aggregate(df, groupby=[], aggregation="sum", column="value"):
    return df.groupby(groupby).agg(
        {column: aggregation}).reset_index()
