import pandas as pd

from comchoice.aggregate.__set_rank import __set_rank
from comchoice.aggregate.__set_card_id import __set_card_id


def win_rate(
    df,
    alternative="alternative",
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    selected="selected",
    show_rank=True,
    voter="voter",
    **kws
):

    df = __set_card_id(
        df.copy(),
        alternative_a=alternative_a,
        alternative_b=alternative_b,
        selected=selected,
        concat="_"
    )
    dd = df.groupby(["option_source", "option_target"])\
        .agg({voter: "count"}).reset_index()

    m = dd.pivot(
        index="option_source",
        columns="option_target",
        values=voter
    ).fillna(0)

    ids = set(df["option_source"]) | set(df["option_target"])
    m = m.reindex(ids)
    m = m.reindex(ids, axis=1)
    m = m.fillna(0)

    r = m + m.T
    values = m.sum() / r.sum()

    output = pd.DataFrame(values).reset_index().rename(
        columns={"option_target": alternative, 0: "value"})

    if show_rank:
        output = __set_rank(output)

    return output
