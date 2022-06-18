from math import floor


def quota(
    method="hare",
    n_votes=1,
    n_seats=1
) -> int:
    if method == "hare":
        return floor(n_votes / n_seats)
    elif method == "imperiali":
        return round(n_votes / (n_seats + 2), 0)
    elif method == "droop":
        return floor(n_votes / (n_seats + 1)) + 1
    elif method == "hagenbach-bischoff":
        return floor(n_votes / (n_seats + 1))
    return 1
