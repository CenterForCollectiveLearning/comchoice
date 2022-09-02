import pandas as pd

from itertools import combinations


def approval(
    df,
    delimiter=",",
    method="proportional",
    n_seats=2,
    ballot="ballot",
    voters="voters"
):
    df = df.copy()

    def harmonic(n):
        if n == 0:
            return 0
        return 1 + sum([1 / i for i in range(2, n + 1)])

    df[ballot] = df[ballot].str.split(delimiter)

    output = []
    for seats in combinations(df[ballot].explode().unique(), n_seats):
        for i, tmp in df.iterrows():
            n_items = len(set(tmp[ballot]) & set(seats))

            if method == "classic":
                coef = 1  # TODO

            elif method == "proportional":
                coef = harmonic(n_items)

            elif method == "satisfaction":
                coef = n_items / \
                    len(set(tmp[ballot])) if n_items > 0 else 0
                if coef > 1:
                    coef = 1

            output.append({
                ballot: seats,
                "value": coef * tmp[voters]
            })

    tmp = pd.DataFrame(output).groupby(
        ballot).agg({"value": "sum"}).reset_index()
    tmp = tmp.sort_values("value", ascending=False)

    return tmp
