import pandas as pd
import re
import urllib


def from_preflib(
    path: str
):
    """Converts Preflib Data
    Parameters
    ----------
    path : str
        Data set URL

    Returns
    -------
    pd.DataFrame, pd.DataFrame
        DataFrame objects of nodes and edges.
    """
    file = urllib.request.urlopen(path)
    arr = file.read().decode("utf-8").split("\n")
    alternatives = list(filter(lambda k: "# ALTERNATIVE NAME" in k, arr))
    alternatives = [x.replace("# ALTERNATIVE NAME ", "").split(": ")
                    for x in alternatives]

    unique_orders = list(
        filter(lambda k: "# NUMBER UNIQUE ORDERS: " in k, arr))[0].split(": ")[1]
    data = list(filter(lambda k: "# " not in k, arr))
    _ = path.split(".")[-1]

    df_nodes = pd.DataFrame(
        alternatives,
        columns=["alternative", "name"]
    )
    df_edges = pd.DataFrame(data).dropna().head(int(unique_orders)).copy()
    df_edges[["voters", 0]] = df_edges[0].str.split(": ", expand=True)
    df_edges["voters"] = df_edges["voters"].astype(int)

    def lambda_row(x):
        row = [item for item in re.split(r",\{(.*?)\}", x[0])[:2]]
        if len(row) < 2:
            row.append(None)
        return row

    if _ in ["toc"]:
        cols = ["winners", "losers"]
        df_edges[cols] = df_edges.apply(
            lambda x: lambda_row(x),
            axis=1,
            result_type="expand"
        )
        for col in cols:
            df_edges[col] = df_edges[col].str.replace(
                "{", "", regex=False).str.replace("}", "", regex=False)

    elif _ in ["soc"]:
        df_edges = df_edges.rename(columns={1: "rank"})

    else:
        cols = ["source", "destination"]
        df_edges[cols] = df_edges[1].str.split(",", expand=True)

    df_edges = df_edges.drop(columns=[0], errors="ignore")

    return df_nodes, df_edges
