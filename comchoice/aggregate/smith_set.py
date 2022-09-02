import numpy as np
import pandas as pd

from comchoice.aggregate.__default_parameters import transform_kws
from comchoice.aggregate.pairwise_matrix import pairwise_matrix


def smith_set(
    df,
    alternative="alternative",
    ballot="ballot",
    delimiter=">",
    voter="voter",
    voters="voters",
    transform_kws=transform_kws
) -> list:
    """Smith Set.

    The Smith Set, Generalized Top-Choice Assumption (GETCHA), or Top Cycle,
    is the smallest non-empty set of alternatives in an election.
    Each member defeats every alternative outside the set in a pairwise election.

    Returns
    -------
    list:
        alternatives that are part of the Smith Set.
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
