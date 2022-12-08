import pandas as pd

from itertools import combinations


def approval(
    df: pd.DataFrame,
    delimiter: str = ",",
    method: str = "proportional",
    n_seats: int = 2,
    ballot: str = "ballot",
    voters: str = "voters"
) -> pd.DataFrame:
    """Approval rule.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ",".
    method : {"classic", "proportional", "satisfaction"}, optional
        Approval method to use, by default "proportional".
    n_seats : int, optional
        Number of seats to elect, by default 2.
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Approval rule.
    """
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
