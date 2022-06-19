import pandas as pd


def to_individual_voter(
    df,
    voters="voters",
    voter="voter"
):
    output = []
    for i, row in df.iterrows():
        tmp = pd.DataFrame([row] * row[voters])
        output.append(tmp)
    df = pd.concat(output, ignore_index=True)
    df[voter] = range(df.shape[0])
    df = df.drop(columns=[voters])

    return df
