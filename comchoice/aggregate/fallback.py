import pandas as pd

from comchoice.aggregate.__set_rank import __set_rank


def fallback(
    df,
    alternatives="alternatives",
    delimiter=",",
    n_seats=1,
    voters="voters"
):

    df[alternatives] = df[alternatives].str.split(delimiter)
    df["_top_ranked"] = df[alternatives].apply(lambda x: x[0])

    tmp = df.groupby("_top_ranked").agg({voters: "sum"}) / df[voters].sum()

    # If there is a top-rated alternative over 50%, that alternative is elected as the winner
    rate_top_ranked = tmp[voters] > 0.5
    if any(rate_top_ranked) and n_seats == 1:
        return tmp[rate_top_ranked].reset_index()

    else:
        tmp = df.copy()
        tmp = tmp.explode(alternatives)
        tmp = tmp.groupby(alternatives).agg({voters: "sum"})
        tmp = tmp.reset_index()

        tmp = __set_rank(tmp)

        tmp["elected"] = tmp["rank"] <= n_seats

        return tmp
