import pandas as pd

from comchoice.aggregate.__set_rank import __set_rank


def fallback(
    df,
    candidates="candidates",
    delimiter=",",
    n_seats=1,
    voters="voters"
):

    df[candidates] = df[candidates].str.split(delimiter)
    df["_top_ranked"] = df[candidates].apply(lambda x: x[0])

    tmp = df.groupby("_top_ranked").agg({voters: "sum"}) / df[voters].sum()

    # If there is a top-rated candidate over 50%, that candidate is elected as the winner
    rate_top_ranked = tmp[voters] > 0.5
    if any(rate_top_ranked) and n_seats == 1:
        return tmp[rate_top_ranked].reset_index()

    else:
        tmp = df.copy()
        tmp = tmp.explode(candidates)
        tmp = tmp.groupby(candidates).agg({voters: "sum"})
        tmp = tmp.reset_index()

        tmp = __set_rank(tmp)

        tmp["elected"] = tmp["rank"] <= n_seats

        return tmp
