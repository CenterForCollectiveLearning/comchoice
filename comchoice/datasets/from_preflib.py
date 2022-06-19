import pandas as pd
import re
import urllib


def from_preflib(path):
    """
    Converts Preflib Data
    """
    file = urllib.request.urlopen(path)
    arr = file.read().decode('utf-8').split("\n")
    _ = path.split(".")[-1]

    output = []
    nodes = int(arr[0])
    for index, line in enumerate(arr):
        output.append(line.split(",", 1))

    df = pd.DataFrame(output).dropna()

    df_nodes = df.head(nodes).copy()
    df_nodes = df_nodes.rename(columns={0: "node_id", 1: "node_name"})
    df_edges = df[nodes+1:df.shape[0]].copy()

    if _ in ["toc"]:
        cols = ["winners", "losers"]
        df_edges[cols] = df_edges.apply(
            lambda x: [item for item in re.split(r",\{(.*?)\}", x[1])[:2]],
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

    df_edges = df_edges.rename(columns={0: "voters"})
    df_edges = df_edges.drop(columns=[1], errors="ignore")

    return df_nodes, df_edges
