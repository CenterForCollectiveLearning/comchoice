import pandas as pd
import numpy as np

def create_random_spread(
    speed = 0.1,
    number_grids = 100
):
    """
    Create random spread

    Returns
    -------
    state: 
        A dictionary of matrices 2D
    """

    state_per_time = {}
    population = np.zeros((number_grids,number_grids))
    total_grids = number_grids * number_grids
    color_per_time = int(total_grids * speed)
    each = 0
    
    while np.sum(np.sum(population)) < total_grids:
        for _ in range(color_per_time):
            i, j = np.random.randint(number_grids, size=2)
            while population[i][j] != 0:
                i, j = np.random.randint(number_grids, size=2)
            population[i][j] = 1

        state_per_time[each] = np.copy(population)
        each = each + 1
    return state_per_time
