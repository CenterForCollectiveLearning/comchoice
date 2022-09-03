from math import floor


def quota(
    method: str = "hare",
    n_votes: int = 1,
    n_seats: int = 1
) -> int:
    """Computes Quota threshold.

    Parameters
    ----------
    method : {"hare", "imperiali", "droop", "hagenbach-bischoff"}
        Specifies the method to compute the quota, by default "hare".
    n_votes : int
        Number of votes, by default 1.
    n_seats : int
        Number of seats to elect, by default 1.

    Returns
    -------
    int
        Quota threshold
    """
    if method == "hare":
        return floor(n_votes / n_seats)
    elif method == "imperiali":
        return round(n_votes / (n_seats + 2), 0)
    elif method == "droop":
        return floor(n_votes / (n_seats + 1)) + 1
    elif method == "hagenbach-bischoff":
        return floor(n_votes / (n_seats + 1))
    return 1
