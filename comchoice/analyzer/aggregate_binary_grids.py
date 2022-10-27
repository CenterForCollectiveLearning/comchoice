import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def aggregate_spatially_grids(
    mystate,
    new_size = 10
):
    """
    Aggregate grids
    """

    size_space = len(mystate)

    number_polls = int((size_space)/new_size)
    newstate =  np.zeros((new_size,new_size))

    print(size_space, new_size, number_polls, np.shape(newstate))
    from_ = 0
    to_ = 0
    for r,row in enumerate(newstate):
        for c,col in enumerate(row): 
            newValue = np.sum(np.sum(mystate[from_:from_+number_polls,to_:to_+number_polls]))/(number_polls*number_polls)
            if newValue > 0.5:
                newstate[r][c] = 1
            else:
                newstate[r][c] = 0
            to_ = to_ + number_polls
        from_ = from_ + number_polls
        to_ = 0
    
    sns.heatmap(newstate, vmin=0, vmax=1, 
            cbar= False, cmap='Blues', linewidth=.5,
            xticklabels=False, yticklabels=False)
    return newstate 

