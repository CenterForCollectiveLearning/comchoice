import numpy as np
import pandas as pd


def phragmen(
    df,
    n_seats=2,
    ballot="ballot",
    delimiter=",",
    voters="voters"
) -> pd.DataFrame:
    # Phragmén’s sequential rule
    df_tmp = df.copy()
    df_tmp["_id"] = range(df_tmp.shape[0])
    # voters = self.voters

    # n_voters = df_tmp[voters].sum()
    n_rows = df_tmp.shape[0]
    W = []

    df_tmp[ballot] = df_tmp[ballot].str.split(delimiter)
    df_tmp = df_tmp.copy()
    df_tmp = df_tmp.explode(ballot)

    dd = 1 / df_tmp.groupby(ballot).agg({voters: "sum"})
    dd = dd.reset_index()
    dd = dd.rename(columns={voters: "t*", ballot: "alternative"})

    t_1 = dd.head(1).to_dict(orient="records")[0]
    W.append(t_1)

    im = df_tmp.pivot(index="_id", columns=ballot).fillna(0)
    columns = [i[1] for i in im.columns]
    im.columns = columns
    im = im.reset_index(drop=True)

    while len(W) < n_seats and n_seats > 0:
        zeros_m = np.zeros((n_rows, len(columns)))
        mi = pd.DataFrame(zeros_m, columns=columns)
        for w in W:
            option = w["alternative"]
            _t = w["t*"]

            for index in im.index.values:
                if im.loc[index, option] > 0:
                    mi.iloc[index] = _t

        output = np.multiply(im, mi).reset_index(drop=True)
        output = np.multiply(1 + output.sum(axis=0), 1 / im.sum(axis=0))

        output = output.sort_values().to_frame("t*")\
            .reset_index().rename(columns={"index": "alternative"})

        filters = [x["alternative"] for x in W]
        output = output[~output["alternative"].isin(filters)]

        t_n = output.head(1).to_dict(orient="records")[0]
        W.append(t_n)

    return pd.DataFrame(W).rename(columns={"t*": "value"}).sort_values("value", ascending=False)
