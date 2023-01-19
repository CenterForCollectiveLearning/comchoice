import pandas as pd
import re
import urllib


def from_preflib(
    path: str,
    get_dataset_metadata: bool = False
):
    """Converts Preflib Data

    Parameters
    ----------
    path : str
        Data set URL
    get_dataset_metadata : bool
        Whether this value is True, it returns a third dict with metadata included in the dataset, by default False.


    Returns
    -------
    pd.DataFrame, pd.DataFrame
        DataFrame objects of nodes and edges.
    """
    file = urllib.request.urlopen(path)
    arr = file.read().decode("utf-8").split("\n")
    alternatives = list(filter(lambda k: "# ALTERNATIVE NAME" in k, arr))
    alternatives = [x.replace("# ALTERNATIVE NAME ", "").split(": ", 1)
                    for x in alternatives]

    def get_preflib_info(key, arr=arr):
        return list(filter(lambda k: f"# {key}: " in k, arr))[0].split(": ", 1)[1]

    unique_orders = get_preflib_info("NUMBER UNIQUE ORDERS")
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

    elif _ in ["soc", "soi"]:
        df_edges = df_edges.rename(columns={0: "ballot"})
        df_edges["ballot"] = df_edges["ballot"].str.replace(",", ">")

    else:
        cols = ["source", "destination"]
        df_edges[cols] = df_edges[1].str.split(",", expand=True)

    df_edges = df_edges.drop(columns=[0], errors="ignore")

    if get_dataset_metadata:
        metadata = {
            "data_type": get_preflib_info("DATA TYPE"),
            "modification_date": get_preflib_info("MODIFICATION DATE"),
            "modification_type": get_preflib_info("MODIFICATION TYPE"),
            "number_alternatives": int(get_preflib_info("NUMBER ALTERNATIVES")),
            "number_unique_orders": int(unique_orders),
            "number_voters": int(get_preflib_info("NUMBER VOTERS")),
            "publication_date": get_preflib_info("PUBLICATION DATE"),
            "title": get_preflib_info("TITLE")
        }
        return df_nodes, df_edges, metadata

    return df_nodes, df_edges
