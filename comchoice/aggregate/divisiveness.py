import numpy as np
import pandas as pd
from tqdm import tqdm

from . import ahp
from comchoice.aggregate.__set_card_id import __set_card_id
from comchoice.aggregate.__set_rank import __set_rank
from comchoice.preprocessing import to_pairwise


def divisiveness(
    df,
    alternative="alternative",
    method=ahp,
    method_kws=dict(),
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    selected="selected",
    convert_pairwise=False,
    show_rank=True,
    verbose=True,
    voter="voter"
):
    """Divisiveness

    Parameters
    ----------
    df : _type_
        _description_
    alternative : str, optional
        _description_, by default "id"
    method : _type_, optional
        _description_, by default borda
    alternative_a : str, optional
        _description_, by default "alternative_a"
    alternative_b : str, optional
        _description_, by default "alternative_b"
    selected : str, optional
        _description_, by default "selected"
    verbose : bool, optional
        _description_, by default True
    voter : str, optional
        _description_, by default "voter"

    Returns
    -------
    _type_
        _description_
    """
    tmp = df.copy()
    df_original = df.copy()
    if convert_pairwise:
        tmp = to_pairwise(tmp, origin="voting")

    tmp = __set_card_id(
        tmp.copy(),
        alternative_a=alternative_a,
        alternative_b=alternative_b,
        selected=selected,
        concat="_"
    )

    dd = tmp.groupby(["card_id", selected, voter]).agg({"id": "count"})
    # _data = df.copy().set_index(voter)

    def _f(idx, df_select):
        card_id = idx[0]
        s = idx[1]
        users = [item[2] for item in df_select.index.to_numpy()]

        # data_temp = _data.loc[users].reset_index()
        data_temp = df_original[df_original[voter].isin(users)]
        r_tmp = method(data_temp, **method_kws).dropna()
        r_tmp["card_id"] = card_id
        r_tmp[selected] = s

        del data_temp, users

        return r_tmp

    tmp_list = []

    _data_tmp = dd.groupby(level=[0, 1])

    _iter = tqdm(_data_tmp, position=0,
                 leave=True) if verbose else _data_tmp

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

    tmp_dv = pd.merge(tmp_a, tmp_b, on=[
                      "card_id", alternative, f"{alternative_a}_sorted", f"{alternative_b}_sorted"])

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
    tmp = tmp[tmp[alternative]
              == tmp["selected"]]
    tmp = tmp.groupby(alternative).agg(
        {"value": "mean"}).reset_index()

    if show_rank:
        tmp = __set_rank(tmp)

    return tmp
