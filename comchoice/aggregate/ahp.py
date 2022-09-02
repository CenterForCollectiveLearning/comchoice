import numpy as np
import pandas as pd
from scipy import linalg

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.__set_card_id import __set_card_id
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.pairwise_matrix import pairwise_matrix
from comchoice.preprocessing.transform import transform


def ahp(
    df,
    ppal_eigval="approximation",
    criteria="criteria",
    delimiter=">",
    origin="ballot",
    alternative="alternative",
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    selected="selected",
    transform_kws=transform_kws,
    show_rank=True,
    **kws
) -> pd.DataFrame:
    """Analytic Hierarchy Process (AHP)

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    ppal_eigval : {"approximation", "eigval"}
        Specifies the method to compute the eigenvector used in the algorithm, by default "approximation"
    criteria : str, optional
        Column label when data set includes more than one election criteria, by default "criteria"
    origin : str, optional
        _description_, by default "pairwise"
    alternative : str, optional
        Defines column label of the output data that includes the score of each alternative, by default "alternative"
    alternative_a : str, optional
        When `origin` is `pairwise`, column label for alternative displayed on the left of a pairwise comparison framework, by default "alternative_a"
    alternative_b : str, optional
        When `origin` is `pairwise`, column label for alternative displayed on the right of a pairwise comparison framework, by default "alternative_b"
    selected : str, optional
        When `origin` is `pairwise`, column label for alternative selected, by default "selected"
    show_rank : bool, optional
        Whether or not to include the ranking of alternatives, by default True.

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using AHP.
    """

    df = df.copy()

    if origin != "pairwise":

        df = transform(
            df.copy(),
            **{
                **transform_kws,
                **dict(
                    dtype_to="pairwise"
                )
            }
        )

        if "card_id" not in list(df):
            df = __set_card_id(
                df.copy(),
                alternative_a=alternative_a,
                alternative_b=alternative_b,
                selected=selected,
                concat="_"
            )

    alternative_a_sorted = f"{alternative_a}_sorted"
    alternative_b_sorted = f"{alternative_b}_sorted"

    if selected in list(df):
        df["weight_a"] = np.where(
            df[alternative_a_sorted] == df[selected], 1, 0)
        df["weight_b"] = np.where(
            df[alternative_b_sorted] == df[selected], 1, 0)

        df = df.groupby([alternative_a_sorted, alternative_b_sorted]).agg(
            {"weight_a": "sum", "weight_b": "sum"}).reset_index()

    def __calc(df, ppal_eigval=ppal_eigval):
        df["value"] = df["weight_b"] / df["weight_a"]

        items = set(df[alternative_a_sorted]) | set(df[alternative_b_sorted])
        n = len(items)

        tmp = df.pivot(index=alternative_b_sorted,
                       columns=alternative_a_sorted, values="value")
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
        priority.columns = [alternative, "value"]

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

    if show_rank:
        priority = __set_rank(priority)

    return priority  # , ci, cr
