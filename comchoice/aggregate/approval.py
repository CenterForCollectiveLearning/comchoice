import pandas as pd
from itertools import combinations


def approval(
    df,
    delimiter=",",
    method="proportional",
    n_seats=2,
    alternatives="alternatives",
    voters="voters"
):
    def harmonic(n):
        if n == 0:
            return 0
        return 1 + sum([1 / i for i in range(2, n + 1)])

    df[alternatives] = df[alternatives].str.split(delimiter)

    output = []
    for seats in combinations(df[alternatives].explode().unique(), n_seats):
        for i, tmp in df.iterrows():
            n_items = len(set(tmp[alternatives]) & set(seats))

            if method == "classic":
                coef = 1  # TODO

            elif method == "proportional":
                coef = harmonic(n_items)

            elif method == "satisfaction":
                coef = n_items / \
                    len(set(tmp[alternatives])) if n_items > 0 else 0
                if coef > 1:
                    coef = 1

            output.append({
                alternatives: seats,
                "value": coef * tmp[voters]
            })

    return pd.DataFrame(output).groupby(alternatives).agg({"value": "sum"}).reset_index()
