import numpy as np
import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.pairwise_matrix import pairwise_matrix


def smith_set(
    df,
    alternative: str = "alternative",
    ballot: str = "ballot",
    delimiter: str = ">",
    voter: str = "voter",
    voters: str = "voters",
    transform_kws: dict = transform_kws
) -> list:
    """Smith Set.

    The Smith Set, Generalized Top-Choice Assumption (GETCHA), or Top Cycle,
    is the smallest non-empty set of alternatives in an election.
    Each member defeats every alternative outside the set in a pairwise election.

    Parameters
    ----------
    df : pd.DataFrame
        A data set to be aggregated.
    alternative : str, optional
        Column label to get alternatives, by default "alternative".
    ballot : str, optional
        Column label that includes a set of sorted alternatives for each voter or voters (when is defined in the data set), by default "ballot".
    delimiter : str, optional
        Delimiter used between alternatives in a `ballot`, by default ">".
    voter : str, optional
        _description_, by default "voter"
    voters : str, optional
        Whether the number of voters is defined in the data, it represents its column label, by default "voters".
    transform_kws : dict, optional
        Whether or not to process data.

    Returns
    -------
    list:
        Alternatives that are part of the Smith Set.
    """

    m = pairwise_matrix(
        df,
        alternative=alternative,
        ballot=ballot,
        delimiter=delimiter,
        voter=voter,
        voters=voters,
        transform_kws=transform_kws
    )
    __index = m.sum(axis="columns").sort_values(ascending=False).index

    m = m.reindex(__index, axis=0)
    m = m.reindex(__index, axis=1)

    _alternatives = list(m)
    m_values = m.values

    _col = _alternatives[0]

    while _col:
        _col_p = _col
        for _row in _alternatives:
            i_row = _alternatives.index(_row)
            i_col = _alternatives.index(_col)

            if i_row > i_col:
                _value = m_values[i_row, i_col]
                if _value > 0:
                    _col = _row
                    break

        if _col_p == _col:
            _col = False

    return _alternatives[:i_col + 1]
