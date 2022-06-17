import pandas as pd
from itertools import combinations


def approval(
    df,
    delimiter=",",
    method="proportional",
    n_seats=2,
    candidates="candidates",
    voters="voters"
):
    def harmonic(n):
        if n == 0:
            return 0
        return 1 + sum([1 / i for i in range(2, n + 1)])

    df[candidates] = df[candidates].str.split(delimiter)

    output = []
    for seats in combinations(df[candidates].explode().unique(), n_seats):
        for i, tmp in df.iterrows():
            n_items = len(set(tmp[candidates]) & set(seats))

            if method == "classic":
                coef = 1  # TODO

            elif method == "proportional":
                coef = harmonic(n_items)

            elif method == "satisfaction":
                coef = n_items / \
                    len(set(tmp[candidates])) if n_items > 0 else 0
                if coef > 1:
                    coef = 1

            output.append({
                candidates: seats,
                "value": coef * tmp[voters]
            })

    return pd.DataFrame(output).groupby(candidates).agg({"value": "sum"}).reset_index()
