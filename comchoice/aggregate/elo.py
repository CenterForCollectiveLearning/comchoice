import pandas as pd


def elo(
    df,
    option_a="option_a",
    option_b="option_b",
    candidate="candidate",
    selected="selected",
    rating: int = 400,
    K: int = 10
):
    """Elo score.

    Calculates a ranking of candidates using Elo rating.

    Parameters
    ----------
    rating : int, default=400
        Initial rating of each candidate.
    K : int, default=10
        The K-factor estimates the score that a player can win in a game.

    """

    candidates = set(df[option_a]) | set(df[option_b])

    ELO_RATING = {i: rating for i in candidates}

    for item_a, item_b, item_selected in list(zip(df[option_a], df[option_b], df[selected])):
        r_a = ELO_RATING[item_a]
        r_b = ELO_RATING[item_b]

        q_a = K ** (r_a / rating)
        q_b = K ** (r_b / rating)

        e_a = q_a / (q_a + q_b)
        e_b = q_b / (q_a + q_b)

        if item_selected == 0:
            s_a = 0.5
            s_b = 0.5

        else:
            is_a_selected = item_a == item_selected
            s_a = 1 if is_a_selected else 0
            s_b = 1 - s_a

        ELO_RATING[item_a] = r_a + K * (s_a - e_a)
        ELO_RATING[item_b] = r_b + K * (s_b - e_b)

    return pd.DataFrame(
        ELO_RATING.items(),
        columns=[candidate, "value"]
    )
