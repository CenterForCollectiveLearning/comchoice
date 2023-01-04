import pandas as pd


def unpack_ballot(
    df,
    voter="voter",
    voters="voters"
):
    data = df.copy()

    if voters in list(df):
        output = []
        for i, row in df.iterrows():
            tmp = pd.DataFrame([row] * row[voters])
            output.append(tmp)
        data = pd.concat(output, ignore_index=True)
        data[voter] = range(data.shape[0])

        data = data.drop(columns=[voters])

    return data
