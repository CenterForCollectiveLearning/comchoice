import numpy as np
import pandas as pd
from itertools import combinations


class Voting:
    def __init__(self, data):
        df = data.copy() if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

        self.candidate = "candidate"
        self.df = df
        self.rank = "rank"
        self.show_rank = True
        self.voter = "voter"
        self.voters = "voters"


    def borda(self):
        """Calculates Borda Count

        Returns:
            pandas.DataFrame: a ranking of candidates using Borda Count. 
        """
        df = self.df.copy()
        candidate = self.candidate
        rank = self.rank
        voters = self.voters
        plural_voters = voters in list(df)

        if plural_voters:
            df = self.transform(df)
        N = len(df[candidate].unique())
        df["value"] = N - df[rank]
        if plural_voters:
            df["value"] *= df[voters]

        tmp = df.groupby(candidate).agg({"value": "sum"}).reset_index().sort_values("value", ascending=False)
        if self.show_rank:
            tmp["rank"] = range(1, tmp.shape[0] + 1)
        return tmp
    
    
    def compare_methods(self, methods=["borda", "k-approval", "copeland", "plurality"]):
        """Compares the ranking given to a candidate in different aggregation methods.

        Args:
            methods (list, optional): Methods to be compared. Values accepted are borda, k-approval, copeland, and plurality.

        Returns:
            pandas.DataFrame: DataFrame with a comparison of the methods defined. The first column represents the candidate, and the following ones represent each method being compared.
        """
        output = pd.DataFrame()
        candidate = self.candidate

        for method in methods:
            r = self.ranking(method=method, k=1)
            r = r.rename(columns={"rank": method})
            r = r[[candidate, method]]
            output = r.copy() if output.shape[0] == 0 else pd.merge(output, r, on=candidate)

        return output
    
    
    def completeness(self):
        """Verifies if the data is complete. That is, every voter selected all the candidates possible.
        
        Returns:
            bool: Boolean variable to indicate if the data is complete.
        """
        df = self.df.copy()

        candidate = self.candidate
        voter = self.voter
        voters = self.voters

        if voters in list(df):
            df = self.transform(df, unique_id=True)
            df = df.rename(columns={"_id": "voter"})
        else:
            df[voters] = 1

        unique_candidates = df[candidate].unique()
        
        for idx, df_tmp in df.groupby([voter, voters]):
            if len(df_tmp[candidate].unique()) != len(unique_candidates):
                return False
            
        return True


    def copeland(self):
        df = self.df.copy()
        output = []

        candidate = self.candidate
        rank = self.rank
        voter = self.voter
        voters = self.voters

        cols = ["_winner", "_loser"]

        if voters in list(df):
            df = self.transform(df, unique_id=True)
            df = df.rename(columns={"_id": "voter"})
        else:
            df[voters] = 1

        unique_candidates = df[candidate].unique()
        for idx, df_tmp in df.groupby([voter, voters]):
            _voter, _voters = idx

            df_tmp = df_tmp.sort_values(rank)
            items = df_tmp[candidate].values

            tmp = pd.DataFrame(list(combinations(items, 2)), columns=cols)
            tmp["value"] = _voters
            output.append(tmp)

        m = pd.concat(output).groupby(cols).agg({"value": "sum"}).reset_index()

        m = m.pivot(index=cols[0], columns=cols[1], values="value")
        m = m.reindex(unique_candidates, axis=0)
        m = m.reindex(unique_candidates, axis=1)
        m = m.fillna(0)

        r = m + m.T
        m = m / r

        m = m > 0.5
        m = m.astype(float)
        np.fill_diagonal(m.values, np.nan)

        tmp = pd.DataFrame([(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=1)))], 
                            columns=[candidate, "value"]).sort_values("value", ascending=False)
        if self.show_rank:
            tmp["rank"] = range(1, tmp.shape[0] + 1)

        return tmp
    
    
    def hare_rule(self):
        """
        Hare Rule, Ranked-Choice Voting, Alternative Vote, and Instant Runoff
        """

        df = self.df.copy()
        candidate = self.candidate
        rank = self.rank
        voters = self.voters

        if voters in list(df):
            df = self.transform(df, unique_id=True)

        def _plurality(df):
            df = df[df["rank"] == 1].copy()
            df["value"] = 1
            if "voters" in list(df):
                df["value"] *= df["voters"]

            return df.groupby(candidate).agg({"value": "sum"}).reset_index()


        tmp = _plurality(df)
        tmp["value"] /= tmp["value"].sum()
        tmp = tmp.sort_values("value", ascending=False).reset_index(drop=True)

        while tmp.loc[0, "value"] <= 0.5:
            rmv = tmp.loc[tmp.shape[0] - 1, candidate]

            df = df[df[candidate] != rmv].copy()
            df = df.sort_values(["_id", rank], ascending=[True, True])
            df[rank] = df.groupby("_id").cumcount() + 1

            tmp = _plurality(df.copy())
            tmp["value"] /= tmp["value"].sum()
            tmp = tmp.sort_values("value", ascending=False).reset_index(drop=True)

        return tmp.head(1)

    
    def k_approval(self, k=1):
        """Calculates k-approval voting method. The method gives 1 if the candidate is ranked over or equal to k. Otherwise, the value given is 0.

        Args:
            k (int, optional): Threshold to score candidates with a value of 1.

        Returns:
            pandas.DataFrame: Values of k-approval method.
        """
        df = self.df.copy()

        candidate = self.candidate
        rank = self.rank
        voters = self.voters
        plural_voters = voters in list(df)

        if plural_voters:
            df = self.transform(df)

        df["value"] = df[rank] <= k
        if plural_voters:
            df["value"] *= df[voters]

        tmp = df.groupby(candidate).agg({"value": "sum"}).reset_index().sort_values("value", ascending=False)
        if self.show_rank:
            tmp["rank"] = range(1, tmp.shape[0] + 1)

        return tmp

    
    def plurality(self):
        """Each voter selects one candidate (or none if voters can abstain), and the candidate(s) with the most votes win.
        """
        df = self.df.copy()
        
        candidate = self.candidate
        rank = self.rank
        voters = self.voters

        if voters in list(df):
            df = self.transform(df)
        df = df[df[rank] == 1]
        df["value"] = 1
        if voters in list(df):
            df["value"] *= df[voters]

        tmp = df.groupby(candidate).agg({"value": "sum"}).reset_index().sort_values("value", ascending=False)
        if self.show_rank:
            tmp[rank] = range(1, tmp.shape[0] + 1)

        return tmp
    
    
    def ranking(self, method="plurality", k=1):
        """Calculates the ranking of candidates usen a given voting method.

        Args:
            method (str, optional): Method to be used for calculating the ranking.
            k (str, optional): Just valid for k-approval method.

        Returns:
            pandas.DataFrame: Ranking of candidates calculated with the method defined.
        """
        methods = {
            "borda": self.borda(),
            "copeland": self.copeland(),
            "k-approval": self.k_approval(k=k),
            "plurality": self.plurality()
        }

        try:
            tmp = methods[method]
            return tmp
        except KeyError as err:
            raise Exception(f"{method} is not a valid method.")
    
    
    def _get_items(self, method="borda", ascending=False, n=1):
        df = self.ranking(method=method)
        return df.sort_values("value", ascending=ascending).head(n).reset_index(drop=True)
    

    def loser(self, method="borda", n=1):
        return self._get_items(method=method, ascending=True, n=n)
    
    
    def winner(self, method="borda", n=1):
        return self._get_items(method=method, ascending=False, n=n)
        
    
    def transform(self, data, unique_id=False):
        df = data.copy()
        df["_id"] = range(df.shape[0])
        df = df.explode("rank")
        df = df.rename(columns={"rank": "candidate"})
        df["rank"] = df.groupby("_id").cumcount() + 1
        if not unique_id:
            df = df.drop(columns=["_id"])

        return df