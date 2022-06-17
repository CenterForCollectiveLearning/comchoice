import numpy as np
import pandas as pd
from tqdm import tqdm

from . import borda


def divisiveness(
    df,
    aggregation=None,
    voter="uuid",
    full=False,
    verbose=True,
    method=borda
):
    """
    Calculates divisiveness measure
    """
    selected = "selected"
    option_a = "option_a"
    option_b = "option_b"
    candidate = "id"
    df = df[(df[option_a] == df[selected]) | (
        df[option_b] == df[selected])].copy()

    dd = df.groupby(["card_id", selected, voter]).agg({"id": "count"})
    _data = df.copy().set_index(voter)

    def method_not_found():
        print(f"No Method {agg} Found!")

    def _f(idx, df_select):
        card_id = idx[0]
        s = idx[1]
        users = [item[2] for item in df_select.index.to_numpy()]

        data_temp = _data.loc[users].reset_index()

        r_tmp = method(data_temp).dropna()
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

    tmp[[f"{option_a}_sorted", f"{option_b}_sorted"]
        ] = tmp["card_id"].str.split("_", expand=True)
    tmp["group"] = tmp[f"{option_a}_sorted"].astype(
        str) == tmp[selected].astype(str)
    tmp["group"] = tmp["group"].replace({True: "A", False: "B"})

    tmp_a = tmp[tmp["group"] == "A"]
    tmp_b = tmp[tmp["group"] == "B"]

    tmp_dv = pd.merge(tmp_a, tmp_b, on=[
                      "card_id", candidate, f"{option_a}_sorted", f"{option_b}_sorted"])
    tmp_dv = tmp_dv[[candidate, "card_id", "value_x",
                     "value_y", f"{selected}_x", f"{selected}_y"]]
    tmp_dv["value"] = abs(tmp_dv["value_x"] - tmp_dv["value_y"])

    tmp_frag_a = tmp_dv[[candidate, f"{selected}_x", "value"]].rename(
        columns={f"{selected}_x": "selected"})
    tmp_frag_b = tmp_dv[[candidate, f"{selected}_y", "value"]].rename(
        columns={f"{selected}_y": "selected"})
    tmp_frag_c = pd.concat([tmp_frag_a, tmp_frag_b])
    tmp_frag_c = tmp_frag_c[tmp_frag_c[candidate]
                            == tmp_frag_c["selected"]]
    tmp_frag_c = tmp_frag_c.groupby(candidate).agg(
        {"value": "mean"}).reset_index()

    return tmp_frag_c
