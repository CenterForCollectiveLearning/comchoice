import numpy as np
import pandas as pd
import tqdm
from scipy import linalg


class Pairwise:
    """Pairwise.

    The class `Pairwise` includes methods to manage pairwise comparison data.
    For instance, allows to rank candidates, to convert rating-based data
    into pairwise comparison data, and calculates divisiveness.

    Attributes
    ----------
    candidate: str
        Column name that includes the candidates.
    card_id : str
        Unique identifier column name of candidates' pairs.
    option_a: str
        Column name of the candidate A.
    option_b: str
        Column name of the candidate B.
    selected: str, default="selected"
        Column name of the candidate selected.
    value: str, default="value"
    voter: str, default="voter"
        Column name of the voter.
    """

    def __init__(self, df):
        self.candidate = "candidate"
        self.card_id = "card_id"
        self.df = df
        self.option_a = "option_a"
        self.option_b = "option_b"
        self.rank = "rank"
        self.selected = "selected"
        self.show_rank = True
        self.value = "value"
        self.voter = "voter"

    def __create_card_id(self, df, concat="_") -> pd.DataFrame:
        """Creates a unique identifier for candidates' pair (card_id).

        Parameters
        ----------
        df : pandas.DataFrame
            Pairwise comparison DataFrame.

        concat : str, default="_"
            String to concatenate options.

        Returns
        -------
        pd.DataFrame
            A pairwise comparison DataFrame with card_id column.
        """
        option_a = self.option_a
        option_b = self.option_b
        selected = self.selected

        option_a_sorted = f"{option_a}_sorted"
        option_b_sorted = f"{option_b}_sorted"

        cols = [option_a, option_b, selected]
        a = df[cols].values

        # Sorts options, always lower value on left column
        df[option_a_sorted] = np.where(a[:, 0] < a[:, 1], a[:, 0], a[:, 1])
        df[option_b_sorted] = np.where(a[:, 0] >= a[:, 1], a[:, 0], a[:, 1])

        _a = df[option_a_sorted]
        _b = df[option_b_sorted]

        df["option_selected"] = np.where(
            _a[:] == a[:, 2], 1, np.where(_b[:] == a[:, 2], -1, 0))

        # Creates card_id
        df["card_id"] = _a.astype(str) + "_" + _b.astype(str)

        # Boolean variable, check if a/b was selected
        df["option_source"] = np.where(a[:, 1] == a[:, 2], a[:, 0], a[:, 1])
        df["option_target"] = np.where(a[:, 0] == a[:, 2], a[:, 0], a[:, 1])

        # Creates option_source / option_target
        selected_zero = df[selected] == 0
        df.loc[selected_zero, "option_source"] = df.loc[selected_zero, option_a]
        df.loc[selected_zero, "option_target"] = df.loc[selected_zero, option_b]

        return df

    def copeland(self):
        """Copeland method (1951)

        Calculates a ranking sorting candidates based on the Condorcet winner.

        Returns
        -------
        pandas.DataFrame :
            Copeland ranking
        """
        candidate = self.candidate
        df = self.df.copy()
        m = self.copeland_matrix(df) > 0.5
        m = m.astype(float)
        np.fill_diagonal(m.values, np.nan)

        return pd.DataFrame(
            [(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=0)))],
            columns=[candidate, "value"]
        )

    def copeland_matrix(self, data: pd.DataFrame, absolute: bool = False):
        """Matrix Condorcet.

        Parameters
        ----------
        data : pandas.DataFrame
            Pairwise data.

        absolute : bool, default="true"
            If value is `true`, returns matrix of wins.

        Returns
        -------
        pandas.DataFrame
            Matrix of pairwise matches.
        """
        voter = self.voter
        dd = data.groupby(["option_source", "option_target"]).agg(
            {voter: "count"}).reset_index()
        m = dd.pivot(index="option_source", columns="option_target",
                     values=voter).fillna(0)
        ids = set(data["option_source"]) | set(data["option_target"])
        m = m.reindex(ids)
        m = m.reindex(ids, axis=1)
        m = m.fillna(0)

        if absolute:
            return m

        r = m + m.T
        return m / r

    def elo(self, rating: int = 400, K: int = 10):
        """Elo score.

        Calculates a ranking of candidates using Elo rating.

        Parameters
        ----------
        rating : int, default=400
            Initial rating of each candidate.
        K : int, default=10
            The K-factor estimates the score that a player can win in a game.

        """
        df = self.df.copy()
        option_a = self.option_a
        option_b = self.option_b
        option_a_sorted = f"{option_a}_sorted"
        option_b_sorted = f"{option_b}_sorted"

        ELO_RATING = {i: rating for i in set(
            df[option_a_sorted]) | set(df[option_b_sorted])}

        for option_a, option_b, selected in list(zip(df[option_a_sorted], df[option_b_sorted], df["option_selected"])):
            r_a = ELO_RATING[option_a]
            r_b = ELO_RATING[option_b]

            q_a = K ** (r_a / rating)
            q_b = K ** (r_b / rating)

            e_a = q_a / (q_a + q_b)
            e_b = q_b / (q_a + q_b)

            if selected == 0:
                s_a = 0.5
                s_b = 0.5
            else:
                is_a_selected = selected == 1
                s_a = 1 if is_a_selected else 0
                s_b = 1 - s_a

            ELO_RATING[option_a] = r_a + K * (s_a - e_a)
            ELO_RATING[option_b] = r_b + K * (s_b - e_b)

        tmp = pd.DataFrame(ELO_RATING.items(), columns=[
                           self.candidate, "value"])

        return tmp

    def fit(self, auto_id=True):
        """Fits a data set to a valid ComChoice data set. 
        It includes columns to the dataset that are required to execute methods defined in the class.

        Parameters
        ----------
        auto_id : bool, default="true"
            If value is `true`, it creates an auto increment primary ID column.
        """
        df = self.df
        df = self.__create_card_id(df)

        if auto_id:
            df["id"] = range(1, df.shape[0] + 1)
        self.df = df

    def win_rate(self, data=None):
        """Win rate (also called weighted Borda rule)

        Calculates the fraction of times a proposal is selected with respect to the total of its occurrences.

        Returns
        -------
        pandas.DataFrame:
            Win Rate
        """
        df = data.copy() if isinstance(data, pd.DataFrame) else self.df.copy()
        df = df[df[self.selected] != 0].copy()
        candidate = self.candidate
        voter = self.voter

        dd = df.groupby(["option_source", "option_target"]).agg(
            {voter: "count"}).reset_index()
        m = dd.pivot(index="option_source",
                     columns="option_target", values=voter).fillna(0)
        ids = set(df["option_source"]) | set(df["option_target"])
        m = m.reindex(ids)
        m = m.reindex(ids, axis=1)
        m = m.fillna(0)

        r = m + m.T
        values = m.sum() / r.sum()

        return pd.DataFrame(values).reset_index().rename(columns={"option_target": candidate, 0: "value"})
