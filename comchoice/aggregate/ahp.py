import numpy as np
import pandas as pd
from scipy import linalg


def ahp(
    df,
    ppal_eigval="approximation",
    criteria="criteria",
    origin="pairwise",
    option_a="option_a",
    option_b="option_b",
    selected="selected"
) -> pd.DataFrame:

    option_a_sorted = f"{option_a}_sorted" if origin == "pairwise" else option_a
    option_b_sorted = f"{option_b}_sorted" if origin == "pairwise" else option_b

    if selected in list(df):
        df["weight_a"] = np.where(
            df[option_a_sorted] == df[selected], 1, 0)
        df["weight_b"] = np.where(
            df[option_b_sorted] == df[selected], 1, 0)

        df = df.groupby([option_a_sorted, option_b_sorted]).agg(
            {"weight_a": "sum", "weight_b": "sum"}).reset_index(drop=True)

    def __calc(df, ppal_eigval=ppal_eigval):
        df["value"] = df["weight_b"] / df["weight_a"]

        items = set(df[option_a_sorted]) | set(df[option_b_sorted])
        n = len(items)

        tmp = df.pivot(index=option_b_sorted,
                       columns=option_a_sorted, values="value")
        tmp = tmp.reindex(items, axis=0)
        tmp = tmp.reindex(items, axis=1)

        tmp = tmp.fillna(0) + (1 / tmp.T).fillna(0)
        np.fill_diagonal(tmp.values, 1)

        sum_cols = tmp.sum(axis=0)
        weight = tmp / tmp.sum(axis=0)
        priority = weight.mean(axis=1)

        if ppal_eigval == "eigval":
            _lambda = linalg.eigvals(tmp)[0].real
        elif ppal_eigval == "approximation":
            _lambda = np.multiply(sum_cols, priority).sum()
        else:
            raise "Value provided to ppal_eigval parameter not valid. Values accepted are 'eigval', 'approximation'"

        priority = pd.DataFrame(priority).reset_index()
        priority.columns = ["option", "value"]

        # Calculates Consistency Index
        ci = (_lambda - n) / (n - 1)

        # Calculates Consistency Ratio
        random_index = {
            1: 0, 2: 0, 3: 0.52, 4: 0.89, 5: 1.11, 6: 1.25, 7: 1.35,
            8: 1.4, 9: 1.45, 10: 1.49, 11: 1.51, 12: 1.54, 13: 1.56, 14: 1.57, 15: 1.58
        }  # Random Consistency Index

        cr = ci / random_index[n]

        return priority, ci, cr

    if criteria in list(df):
        output = []
        for i, df_tmp in df.groupby(criteria):
            priority, ci, cr = __calc(df_tmp, ppal_eigval=ppal_eigval)
            priority[criteria] = i
            output.append(priority)

        df_output = pd.concat(output)
        df_output = df_output.reset_index()
        return df_output, ci, cr

    priority, ci, cr = __calc(df, ppal_eigval=ppal_eigval)

    return priority, ci, cr
