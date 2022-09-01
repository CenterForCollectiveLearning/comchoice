import networkx as nx
import pandas as pd


def to_ballot(
    df,
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    ballot="ballot",
    delimiter=">",
    dtype="pairwise",
    score="score",
    score_delimiter="=",
    selected="selected",
    voter="voter"
):
    df["_id"] = range(df.shape[0])

    if dtype == "pairwise":
        output = []
        for v, tmp in df.groupby(voter):
            l = tmp.apply(lambda x:
                          (x[alternative_a], x[alternative_b]) if x[alternative_a] == x[selected] else (
                              x[alternative_b], x[alternative_a]),
                          axis=1
                          )

            DG = nx.DiGraph(list(l))
            TR = nx.transitive_reduction(DG)
            edges = list(TR.edges)

            chain = edges[0]
            for i in range(0, len(edges) - 1):
                b = edges[i + 1]
                if chain[len(chain) - 1] == b[0]:
                    chain = ((*chain, b[1]))

            output.append((v, (delimiter).join(map(str, chain))))

        return pd.DataFrame(output, columns=[voter, "ballot"])

    elif dtype == "score":
        df["alternative"] = df[ballot].str.split(delimiter)
        df = df.explode("alternative")

        df[["alternative", score]] = df["alternative"].str.split(
            score_delimiter, n=1, expand=True)
        df[score] = df[score].astype(float)
        df = df.drop(columns=[ballot])

        return df
