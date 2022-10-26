import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_states(
    states,
    nrows = 2
):
    """
    Plot heatmap states
    """

    ncols = int(len(states)/nrows)
    fig, ax  = plt.subplots(ncols=ncols, nrows=nrows, figsize=(4*ncols,4*nrows))
    nrow = 0
    for x in states:
        if (x>0) and (x%ncols == 0):
            nrow = nrow+1
        c, r = x%ncols, nrow
        sns.heatmap(states[x], vmin=0, vmax=1, 
            ax= ax[r][c], cbar= False, cmap='Blues', linewidth=.5,
            xticklabels=False, yticklabels=False)
        ax[r][c].set_title("iteration=%s"%x)
        ax[r][c].invert_yaxis()

