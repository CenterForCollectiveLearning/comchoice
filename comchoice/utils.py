import pandas as pd


def corr(
    rules,
    candidate="candidate",
    column="rank",
    method="kendall"
) -> pd.DataFrame:
    """Calculates correlation.

    Parameters
    ----------
    rules : dict
        Required.
    candidate : str, optional
        _description_, by default "candidate"
    column : str, optional
        _description_, by default "rank"
    method : str, optional
        _description_, by default "kendall"

    Returns
    -------
    pd.DataFrame
        _description_
    """
    output = []
    for key in rules.keys():
        tmp = rules[key][[candidate, column]]
        tmp["rule"] = key
        output.append(tmp)

    df = pd.concat(output, axis=0).pivot(
        index=candidate, columns="rule", values=column)
    df = df.reset_index()

    return df.corr(method)
