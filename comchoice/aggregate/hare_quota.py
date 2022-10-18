from comchoice.aggregate.quota import quota


def hare_quota(
    n_votes: int = 1,
    n_seats: int = 1
):
    """Computes Hare Quota threshold.

    Parameters
    ----------
    n_votes : int
        Number of votes, by default 1.
    n_seats : int
        Number of seats to elect, by default 1.

    Returns
    -------
    int
        Hare Quota threshold
    """
    return quota(
        method="hare",
        n_votes=n_votes,
        n_seats=n_seats
    )
