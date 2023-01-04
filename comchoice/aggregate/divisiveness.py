import numpy as np
import pandas as pd
from itertools import combinations
from tqdm import tqdm

from . import ahp
from comchoice.aggregate.__set_card_id import __set_card_id
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.preprocessing import unpack_ballot, to_pairwise


# TODO: Calculate Divisiveness with the Score
def divisiveness(
    df: pd.DataFrame,
    alternative: str = "alternative",
    alternative_a: str = "alternative_a",
    alternative_b: str = "alternative_b",
    convert_pairwise: bool = False,
    convert_pairwise_kws: dict = dict(),
    dtype: str = "pairwise",
    method=ahp,
    method_kws: dict = dict(),
    selected: str = "selected",
    show_rank: bool = True,
    verbose: bool = True,
    voter: str = "voter"
):
    """Divisiveness. Navarrete et al. (2022)

    This method allows to calculate divisive alternatives in a set of preferences without relying in any self-reported data.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    method : comchoice.function, optional
        Method used to calculate divisiveness, by default borda.
    alternative_a : str, optional
        Whether a pairwise dataset is given, it represents the first alternative included in the comparison, by default "alternative_a".
    alternative_b : str, optional
        Whether a pairwise dataset is given, it represents the second alternative included in the comparison, by default "alternative_b".
    selected : str, optional
        Whether a pairwise dataset is given, it represents the selected alternative included in the comparison, by default "selected". Ties between alternatives are represent with the value 0.
    verbose : bool, optional
        Whether the value is `True`, it returns an output with the progress of the calculation. by default True.
    voter : str, optional
        Column label of voter unique identifier, by default "voter".

    Returns
    -------
    pd.DataFrame
        Aggregation of preferences using Divisiveness.

    References
    ----------
    Navarrete, C., Ferrada, N., Macedo, M., Colley, R., Zhang, J., Grandi, U., Lang, J., & Hidalgo, C.A. (2022). Understanding Political Agreements and Disagreements: Evidence from the 2022 French Presidential Election.
    """
    df_source = df.copy()

    if dtype == "ballot":
        df_source = unpack_ballot(df_source)

    df_pairwise = df_source.copy()

    convert_pairwise = dtype != "pairwise"

    if convert_pairwise:
        df_pairwise = to_pairwise(
            df_pairwise,
            **convert_pairwise_kws,
            dtype=dtype
        )

    if "card_id" not in list(df_pairwise):
        df_pairwise = __set_card_id(
            df_pairwise.copy(),
            alternative_a=alternative_a,
            alternative_b=alternative_b,
            selected=selected,
            concat="_"
        )

    if dtype in ["ballot", "ballot_extended"]:
        df_source["_pairs"] = df_source["ballot"]\
            .apply(lambda x: list(combinations(x.split(">"), 2)))\
            .apply(lambda x: ["_".join(w) for w in x])

    dd = df_pairwise.groupby(["card_id", selected, voter]).agg({"id": "count"})
    # _data = df.copy().set_index(voter)
    alternatives = set(df_pairwise[alternative_a]) | set(
        df_pairwise[alternative_b])

    def _f(idx, df_select):
        card_id = idx[0]
        s = idx[1]
        users = [item[2] for item in df_select.index.to_numpy()]

        # data_temp = _data.loc[users].reset_index()
        data_temp = df_source[df_source[voter].isin(users)]

        r_tmp = method(data_temp, **method_kws).dropna()
        r_tmp["card_id"] = card_id
        r_tmp[selected] = s

        del data_temp, users

        return r_tmp

    tmp_list = []

    _data_tmp = dd.groupby(level=[0, 1])

    _iter = tqdm(
        _data_tmp,
        position=0,
        leave=True
    ) if verbose else _data_tmp

    for idx, df_select in _iter:
        tmp_list.append(_f(idx, df_select))

    tmp = pd.concat(tmp_list, ignore_index=True)

    tmp[[f"{alternative_a}_sorted", f"{alternative_b}_sorted"]
        ] = tmp["card_id"].str.split("_", expand=True)
    tmp["group"] = tmp[f"{alternative_a}_sorted"].astype(
        str) == tmp[selected].astype(str)
    tmp["group"] = tmp["group"].replace({True: "A", False: "B"})

    tmp_a = tmp[tmp["group"] == "A"]
    tmp_b = tmp[tmp["group"] == "B"]

    tmp_dv = pd.merge(
        tmp_a,
        tmp_b,
        on=["card_id", alternative,
            f"{alternative_a}_sorted", f"{alternative_b}_sorted"]
    )

    tmp_dv = tmp_dv[[alternative, "card_id", "value_x",
                     "value_y", f"{selected}_x", f"{selected}_y"]]
    tmp_dv["value"] = tmp_dv["value_x"] - tmp_dv["value_y"]
    tmp_dv["value"] = tmp_dv["value"] ** 2
    tmp_dv["value"] = np.sqrt(tmp_dv["value"])

    tmp_frag_a = tmp_dv[[alternative, f"{selected}_x", "value"]].rename(
        columns={f"{selected}_x": "selected"})
    tmp_frag_b = tmp_dv[[alternative, f"{selected}_y", "value"]].rename(
        columns={f"{selected}_y": "selected"})
    tmp = pd.concat([tmp_frag_a, tmp_frag_b])
    tmp = tmp[tmp[alternative] == tmp["selected"]]
    tmp = tmp.groupby(alternative).agg(
        {"value": "mean"})

    tmp = tmp.reindex(alternatives, index=1).fillna(0)
    tmp = tmp.reset_index()

    if show_rank:
        tmp = __set_rank(tmp)

    return tmp
