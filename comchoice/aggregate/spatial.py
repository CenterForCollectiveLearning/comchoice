from math import floor
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from comchoice.aggregate import elo,condorcet, copeland, plurality

def spatial(
    data,
    method: str = "condorcet",
    column_group: str = "grid_list",
    delimiter: str = ",",
    showHeatmap: bool = True
) -> int:
    """Computes Spatial threshold.

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
    winners = []
    for grid in data[column_group].unique():
        winner =  []
        if method == "elo":
            winner  =  elo(data[data[column_group]==grid]).sort_values(by='rank').head(1)
        elif method == "copeland":
            winner  =  copeland(data[data[column_group]==grid]).sort_values(by='rank').head(1)
        elif method == "condorcet":
            winner  =  condorcet(data[data[column_group]==grid]).sort_values(by='rank').head(1)
        elif method == "plurality":
            winner  =  plurality(data[data[column_group]==grid]).sort_values(by='rank').head(1)
        
        if len(winner) > 0:
            winners.append([winner['alternative'].values[0], grid])
        else:
            winners.append([None, grid])
        
    winners = pd.DataFrame(winners, columns=["winner",column_group])
    
    if showHeatmap:
        plt.figure()
        if column_group == "grid_list":
            winners['x'] = winners[column_group].apply(lambda x: x[0])
            winners['y'] = winners[column_group].apply(lambda x: x[1])
        elif column_group == "grid_split":
            winners['x'] = winners[column_group].apply(str).str.split(delimiter, expand=True)[0]
            winners['y'] = winners[column_group].apply(str).str.split(delimiter, expand=True)[1]
        winners = winners.sort_values(by="winner", ascending=False)
        winners['cat'] = pd.Categorical(winners["winner"]).codes
        winners
        
        value_to_int = {j:i for i,j in enumerate(pd.unique(winners["winner"].ravel()))}
        n = len(value_to_int)     
        cmap = sns.color_palette("hsv", n)
        ax = sns.heatmap(winners.pivot_table(index="y",columns="x",values='cat', \
            aggfunc=np.unique), cmap=cmap)
        colorbar = ax.collections[0].colorbar 
        r = colorbar.vmax - colorbar.vmin 
        colorbar.set_ticks([colorbar.vmin + r / n * (0.5 + i) for i in range(n)])
        colorbar.set_ticklabels(list(value_to_int.keys())) 
        ax.set_title(method)

    return winners[["winner",column_group]]
