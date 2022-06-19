import pandas as pd

from .__transform import __transform


def coombs(
    df,
    delimiter=">",
    voters="voters"
) -> str:
    n_voters = df[voters].sum()

    def count_by_rank(df, delimiter=">", rmv=[], n_voters=n_voters):
        tmp = __transform(df, delimiter=delimiter, rmv=rmv)
        tmp = tmp.groupby(["candidate", "rank"]).agg(
            {voters: "sum"}) / n_voters
        return tmp.reset_index()

    tmp = count_by_rank(df, delimiter=delimiter)
    tmp_ranked_first = tmp[tmp["rank"] == 1]

    rmv = []
    n_candidates = tmp["candidate"].unique()

    while not any(tmp_ranked_first[voters] >= 0.5):
        tmp_lowest_ranked = tmp[tmp["rank"] == (len(n_candidates) - len(rmv))]

        max_rate = tmp_lowest_ranked[voters].max()
        s = tmp_lowest_ranked[tmp_lowest_ranked[voters]
                              >= max_rate]["candidate"].unique()
        rmv += list(s)

        tmp = count_by_rank(df, delimiter=delimiter, rmv=rmv)

        tmp_ranked_first = tmp[tmp["rank"] == 1]

    return tmp_ranked_first.sort_values(voters, ascending=False).head(1)["candidate"].unique()[0]