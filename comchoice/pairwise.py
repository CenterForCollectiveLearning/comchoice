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

    def ahp(self, ppal_eigval="approximation", criteria="criteria", origin="pairwise"):
        df = self.df.copy()
        option_a = self.option_a
        option_b = self.option_b
        selected = self.selected

        option_a_sorted = f"{option_a}_sorted" if origin == "pairwise" else option_a
        option_b_sorted = f"{option_b}_sorted" if origin == "pairwise" else option_b

        if selected in list(df):
            df["weight_a"] = np.where(
                df[option_a_sorted] == df[selected], 1, 0)
            df["weight_b"] = np.where(
                df[option_b_sorted] == df[selected], 1, 0)

            df = df.groupby([option_a_sorted, option_b_sorted]).agg(
                {"weight_a": "sum", "weight_b": "sum"}).reset_index(drop=True)

        def __calc(df, ppal_eigval=ppal_eigval):
            df["value"] = df["weight_b"] / df["weight_a"]

            items = set(df[option_a_sorted]) | set(df[option_b_sorted])
            n = len(items)

            tmp = df.pivot(index=option_b_sorted,
                           columns=option_a_sorted, values="value")
            tmp = tmp.reindex(items, axis=0)
            tmp = tmp.reindex(items, axis=1)

            tmp = tmp.fillna(0) + (1 / tmp.T).fillna(0)
            np.fill_diagonal(tmp.values, 1)

            sum_cols = tmp.sum(axis=0)
            weight = tmp / tmp.sum(axis=0)
            priority = weight.mean(axis=1)

            if ppal_eigval == "eigval":
                _lambda = linalg.eigvals(tmp)[0].real
            elif ppal_eigval == "approximation":
                _lambda = np.multiply(sum_cols, priority).sum()
            else:
                raise "Value provided to ppal_eigval parameter not valid. Values accepted are 'eigval', 'approximation'"

            priority = pd.DataFrame(priority).reset_index()
            priority.columns = ["option", "value"]

            # Calculates Consistency Index
            ci = (_lambda - n) / (n - 1)

            # Calculates Consistency Ratio
            random_index = {
                1: 0, 2: 0, 3: 0.52, 4: 0.89, 5: 1.11, 6: 1.25, 7: 1.35,
                8: 1.4, 9: 1.45, 10: 1.49, 11: 1.51, 12: 1.54, 13: 1.56, 14: 1.57, 15: 1.58
            }  # Random Consistency Index

            cr = ci / random_index[n]

            return priority, ci, cr

        if criteria in list(df):
            output = []
            for i, df_tmp in df.groupby(criteria):
                priority, ci, cr = __calc(df_tmp, ppal_eigval=ppal_eigval)
                priority[criteria] = i
                output.append(priority)

            df_output = pd.concat(output)
            df_output = df_output.reset_index()
            return df_output, ci, cr

        priority, ci, cr = __calc(df, ppal_eigval=ppal_eigval)

        return priority, ci, cr

    def bradley_terry(self, iterations: int = 1) -> pd.DataFrame:
        """Bradley-Terry model (1952)

        Parameters
        ----------
        iterations : int, optional
            _description_, by default 1

        Returns
        -------
        pd.DataFrame
            _description_

        References
        ----------
        Bradley, Ralph Allan; Terry, Milton E. (1952). "Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons". Biometrika. 39 (3/4): 324–345. doi:10.2307/2334029. JSTOR 2334029.
        """
        self.fit()  # Creates custom columns into the dataset
        df = self.df.copy()

        m = self.copeland_matrix(df, absolute=True)
        m = m.values

        candidate = self.candidate
        option_a = self.option_a
        option_b = self.option_b
        rank = self.rank

        ids = set(df[option_a]) | set(df[option_b])
        N = len(ids)

        p = np.ones(N)
        pp = np.zeros(N)

        for _ in range(iterations):
            for i in range(N):
                num = 0
                den = 0
                for j in range(N):
                    num += m[j, i]
                    den += (m[i, j] + m[j, i]) / (p[i] + p[j])

                pp[i] = num / den
            p = pp

        tmp = pd.DataFrame(p / p.sum(), index=ids, columns=["value"]).reset_index()\
            .rename(columns={"index": candidate}).sort_values("value", ascending=False)
        if self.show_rank:
            tmp[rank] = range(1, tmp.shape[0] + 1)

        return tmp

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

    def to_pairwise(self, progress=True):
        """Converts a star rating dataset to a pairwise comparison dataset.

        Parameters
        ----------
        progress : bool, default="true"
            If `value` is true, it displays a progress bar for iteration.

        Returns
        -------
        pandas.DataFrame :
            Pairwise comparison data
        """
        df = self.df

        candidate = self.candidate
        option_a = self.option_a
        option_b = self.option_b
        selected = self.selected
        value = self.value
        voter = self.voter

        _data_tmp = df.groupby(voter)
        _iter = tqdm.tqdm(_data_tmp, position=0,
                          leave=True) if progress else _data_tmp

        output = []
        for user_id, df_tmp in _iter:
            tmp = pd.merge(df_tmp, df_tmp, on=voter, how="outer")
            tmp = tmp[tmp[f"{candidate}_x"] != tmp[f"{candidate}_y"]]
            tmp = tmp[tmp[f"{candidate}_x"] > tmp[f"{candidate}_y"]]
            output.append(tmp)
            del tmp

        tmp = pd.concat(output)
        tmp = tmp.rename(
            columns={f"{candidate}_x": option_a, f"{candidate}_y": option_b})
        tmp["selected"] = np.where(
            tmp[f"{value}_x"] == tmp[f"{value}_y"], 0,
            np.where(tmp[f"{value}_x"] > tmp[f"{value}_y"],
                     tmp[option_a], tmp[option_b])
        )

        self.df = tmp[[voter, option_a, option_b, selected]]

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
