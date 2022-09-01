import numpy as np
import pandas as pd

from comchoice.preprocessing.ballot_extend import ballot_extend
from comchoice.preprocessing.score_extend import score_extend
from comchoice.preprocessing.to_ballot import to_ballot
from comchoice.preprocessing.to_pairwise import to_pairwise


def transform(
    df,
    dtype_from="ballot",
    dtype_to="ballot_extended",
    delimiter=">",
    delimiter_ties="=",
    delimiter_score="=",
    alternative="alternative",
    alternative_a="alternative_a",
    alternative_b="alternative_b",
    selected="selected",
    value="value",
    voter="voter",
    voters="voters",
    ballot="ballot",
    rmv=[],
    unique_id=False,
    ascending=False
):
    if dtype_from == "ballot" and dtype_to == "ballot_extended":
        return ballot_extend(
            df,
            ballot=ballot,
            delimiter=delimiter,
            delimiter_ties=delimiter_ties,
            rmv=rmv,
            unique_id=unique_id
        )

    elif dtype_from == "score" and dtype_to == "score_extended":
        return score_extend(
            df,
            delimiter=delimiter,
            ballot=ballot,
            delimiter_score=delimiter_score,
            unique_id=unique_id,
            ascending=ascending
        )

    elif dtype_from == "pairwise":
        df = to_ballot(
            df,
            ballot=ballot,
            delimiter=delimiter,
            dtype=dtype_from,
            delimiter_score=delimiter_score,
            selected=selected,
            voter=voter
        )
        if dtype_to == "ballot_extended":
            return ballot_extend(
                df,
                ballot=ballot,
                delimiter=delimiter,
                delimiter_ties=delimiter_ties,
                rmv=rmv,
                unique_id=unique_id
            )
        return df

    elif dtype_from in ["ballot", "score"] and dtype_to == "pairwise":
        dtype_a, dtype_b = dtype_from.split("_")
        return to_pairwise(
            df,
            alternative=alternative,
            ascending=ascending,
            delimiter=delimiter,
            alternative_a=alternative_a,
            alternative_b=alternative_b,
            selected=selected,
            ballot=ballot,
            value=value,
            voter=voter,
            voters=voters,
            dtype=dtype_a,
            verbose=True
        )
