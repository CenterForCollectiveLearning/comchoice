import numpy as np
import pandas as pd
from itertools import combinations

class Voting:
    """Class Voting.

    Attributes
    ----------
    candidate: str
        Candidates' column name. The data by default is `candidate`.
    party: str
        Column name that includes the party (used in case of proportional methods).
    rank: str
        Column name that indicates the ranking of preferences.
    show_rank: bool, default=True
        If the value is `true`, the voting method will include a column with each candidate's ranking.
    voter: str
        Column name that includes the preferences of a voter.
    voters: str
        Column name that includes the number of voters that selected the same ranking of preferences.
 
    """
    def __init__(self, data):
        df = data.copy() if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

        self.candidate = "candidate"
        self.df = df
        self.party = "party"
        self.rank = "rank"
        self.show_rank = True
        self.voter = "voter"
        self.voters = "voters"


    def borda(self, score="original") -> pd.DataFrame:
        """Calculates Borda Count.

        Parameters
        ----------
        score: {"original", "score_n", "dowdall"}, default="original"
            Method to calculate Borda score.s

        Returns
        -------
        pandas.DataFrame: 
            a ranking of candidates using Borda Count. 

        References
        ----------
        Borda, J. D. (1784). Mémoire sur les élections au scrutin. Histoire de l'Academie 
        Royale des Sciences pour 1781 (Paris, 1784).
        """
        df = self.df.copy()
        candidate = self.candidate
        rank = self.rank
        voters = self.voters
        plural_voters = voters in list(df)

        if plural_voters:
            df = self.__transform(df)
        N = len(df[candidate].unique())

        if score == "dowdall":
            df["value"] = 1 / df[rank]

        elif score == "score_n":
            df["value"] = N - df[rank] - 1

        else:
            df["value"] = N - df[rank]

        if plural_voters:
            df["value"] *= df[voters]

        tmp = df.groupby(candidate).agg({"value": "sum"}).reset_index().sort_values("value", ascending=False)
        if self.show_rank:
            tmp["rank"] = range(1, tmp.shape[0] + 1)
        return tmp


    def bootstraping(self, iter=1000) -> pd.DataFrame:
        return
    
    
    def compare_methods(self, methods=["borda", "k-approval", "copeland", "plurality"]) -> pd.DataFrame:
        """Compares the ranking given to a candidate in different aggregation methods.

        Parameters
        ----------
        methods : list of {"borda", "k-approval", "copeland", "plurality"}, optional: 
            Methods to be compared. Values accepted are borda, k-approval, copeland, and plurality.

        Returns
        -------
        pandas.DataFrame: 
            DataFrame with a comparison of the methods defined. The first column represents the candidate, and the following ones represent each method being compared.
        """
        output = pd.DataFrame()
        candidate = self.candidate

        for method in methods:
            r = self.ranking(method=method, k=1)
            r = r.rename(columns={"rank": method})
            r = r[[candidate, method]]
            output = r.copy() if output.shape[0] == 0 else pd.merge(output, r, on=candidate)

        return output
    
    
    def completeness(self) -> bool:
        """Verifies if the data is complete. That is, every voter selected all the candidates possible.
        
        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """
        df = self.df.copy()

        candidate = self.candidate
        voter = self.voter
        voters = self.voters

        if voters in list(df):
            df = self.__transform(df, unique_id=True)
            df = df.rename(columns={"_id": "voter"})
        else:
            df[voters] = 1

        unique_candidates = df[candidate].unique()
        
        for idx, df_tmp in df.groupby([voter, voters]):
            if len(df_tmp[candidate].unique()) != len(unique_candidates):
                return False
            
        return True


    def copeland_matrix(self):
        df = self.df.copy()
        output = []

        candidate = self.candidate
        rank = self.rank
        voter = self.voter
        voters = self.voters

        cols = ["_winner", "_loser"]

        def __transform(data, unique_id=False) -> pd.DataFrame:
            df = data.copy()
            df["_id"] = range(df.shape[0])
            df = df.explode("rank")
            df = df.rename(columns={"rank": "candidate"})
            df["rank"] = df.groupby("_id").cumcount() + 1
            if not unique_id:
                df = df.drop(columns=["_id"])

            return df

        if voters in list(df):
            df = __transform(df, unique_id=True)
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

        m = np.where(m > 0.5, 1, np.where(m == 0.5, 0.5, 0))
        m = m.astype(float)
        np.fill_diagonal(m, np.nan)

        return pd.DataFrame(m, index=unique_candidates, columns=unique_candidates)


    def copeland(self) -> pd.DataFrame:
        """Calculates Copeland.

        Returns
        -------
        pandas.DataFrame: 
            a ranking of candidates using Copeland. 
            
        """
        df = self.df.copy()
        candidate = self.candidate

        m = self.copeland_matrix(df)

        tmp = pd.DataFrame([(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=1)))], 
                            columns=[candidate, "value"]).sort_values("value", ascending=False)
        if self.show_rank:
            tmp["rank"] = range(1, tmp.shape[0] + 1)

        return tmp


    def cumulative(self) -> pd.DataFrame:
        """Calculates the cumulative score of each candidate (Cumulative Voting).
        """
        candidate = self.candidate
        rank = self.rank
        votes = self.votes
        df = self.df.copy()
        tmp = df.groupby(candidate).agg({votes: "sum"}).reset_index().rename(columns={votes: "value"}).sort_values("value", ascending=False)
        if self.show_rank:
            tmp[rank] = range(1, tmp.shape[0] + 1)

        return tmp


    def dowdall(self) -> pd.DataFrame:
        """Dowdall.
        """
        return self.borda(score="dowdall")


    def dhondt(self, seats=1) -> pd.DataFrame:
        """Calculates the number of elected candidates of each party using the D'Hondt (or Jefferson) method.

        Parameters
        ----------
        seats : int, default=1, optional: 
            Number of seats to be assigned in the election.

        Returns
        -------
        pandas.DataFrame: 
            Summary with the seats of each party.
        """
        df = self.df.copy()
        party = self.party
        output = []
        for __party, df_tmp in df.groupby(party):
            votes = df_tmp.votes.values[0]
            for i in range(seats):
                output.append({party: __party, "quot": votes / (i + 1)})
            
        tmp = pd.DataFrame(output).sort_values("quot", ascending=False)
        return tmp.head(seats).groupby(party).count().reset_index().rename(columns={"quot": "seats"})
    
    
    def hare(self) -> pd.DataFrame:
        """Calculates the winner of an election using Hare Rule, also called as Instant Runoff, Ranked-Choice Voting, and Alternative Vote.
        In each iteration, removes the candidate with the lowest score in a plurality rule, until to have a majority winner.
        """
        df = self.df.copy()
        candidate = self.candidate
        rank = self.rank
        voters = self.voters

        if voters in list(df):
            df = self.__transform(df, unique_id=True)

        def __plurality(df):
            df = df[df["rank"] == 1].copy()
            df["value"] = 1
            if "voters" in list(df):
                df["value"] *= df["voters"]

            return df.groupby(candidate).agg({"value": "sum"}).reset_index()


        tmp = __plurality(df)
        tmp["value"] /= tmp["value"].sum()
        tmp = tmp.sort_values("value", ascending=False).reset_index(drop=True)

        while tmp.loc[0, "value"] <= 0.5:
            rmv = tmp.loc[tmp.shape[0] - 1, candidate]

            df = df[df[candidate] != rmv].copy()
            df = df.sort_values(["_id", rank], ascending=[True, True])
            df[rank] = df.groupby("_id").cumcount() + 1

            tmp = __plurality(df.copy())
            tmp["value"] /= tmp["value"].sum()
            tmp = tmp.sort_values("value", ascending=False).reset_index(drop=True)

        return tmp.head(1)

    
    def k_approval(self, k=1) -> pd.DataFrame:
        """Calculates k-approval voting method. The method gives 1 if the candidate 
        is ranked over or equal to k. Otherwise, the value given is 0.

        Parameters
        ----------
        k (int, optional): 
            Threshold to score candidates with a value of 1.

        Returns
        -------
        pandas.DataFrame: 
            Values of k-approval method.

        References
        ----------

        """
        df = self.df.copy()

        candidate = self.candidate
        rank = self.rank
        voters = self.voters
        plural_voters = voters in list(df)

        if plural_voters:
            df = self.__transform(df)

        df["value"] = df[rank] <= k
        if plural_voters:
            df["value"] *= df[voters]

        tmp = df.groupby(candidate).agg({"value": "sum"}).reset_index().sort_values("value", ascending=False)
        if self.show_rank:
            tmp["rank"] = range(1, tmp.shape[0] + 1)

        return tmp


    def negative(self) -> pd.DataFrame:
        """Calculates the score of each candidate using Negative Voting.

        Returns
        -------
        pandas.DataFrame: 
            Values of Negative Voting.

        """
        candidate = self.candidate
        rank = self.rank
        votes = self.votes
        df = self.df.copy()

        tmp = df.groupby(candidate).agg({votes: "sum"}).reset_index().rename(columns={votes: "value"}).sort_values("value", ascending=False)
        if self.show_rank:
            tmp[rank] = range(1, tmp.shape[0] + 1)

        return tmp

    
    def plurality(self):
        """Each voter selects one candidate (or none if voters can abstain), and the candidate(s) with the most votes win.
        """
        df = self.df.copy()
        
        candidate = self.candidate
        rank = self.rank
        voters = self.voters

        if voters in list(df):
            df = self.__transform(df)
        df = df[df[rank] == 1]
        df["value"] = 1
        if voters in list(df):
            df["value"] *= df[voters]

        tmp = df.groupby(candidate).agg({"value": "sum"}).reset_index().sort_values("value", ascending=False)
        if self.show_rank:
            tmp[rank] = range(1, tmp.shape[0] + 1)

        return tmp


    def score(self) -> pd.DataFrame:
        """Calculates the score of each candidate--Score Voting--. Also called as Range Voting.
        """
        candidate = self.candidate
        rank = self.rank
        votes = self.votes
        df = self.df.copy()
        tmp = df.groupby(candidate).agg({votes: "mean"}).reset_index().rename(columns={votes: "value"}).sort_values("value", ascending=False)
        if self.show_rank:
            tmp[rank] = range(1, tmp.shape[0] + 1)

        return tmp


    def smith_set(self):
        """The Smith Set, Generalized Top-Choice Assumption (GETCHA), or Top Cycle, 
        is the smallest non-empty set of candidates in an election. 
        Each member defeats every candidate outside the set in a pairwise election. 
        
        Returns
        -------
        list:
            Candidates that are part of the Smith Set.
        """
        
        df = self.df.copy()
        output = []
        m = self.copeland_matrix(df)
        __index = m.sum(axis="columns").sort_values(ascending=False).index

        m = m.reindex(__index, axis=0)
        m = m.reindex(__index, axis=1)

        _candidates = list(m)
        m_values = m.values

        _col = _candidates[0]


        while _col:
            _col_p = _col
            for _row in _candidates:
                i_row = _candidates.index(_row) 
                i_col = _candidates.index(_col)

                if i_row > i_col:
                    _value = m_values[i_row, i_col]
                    if _value > 0:
                        _col = _row
                        break

            if _col_p == _col:
                _col = False

        return _candidates[:i_col + 1]


    def ranking(self, method="plurality", k=1, bootstrap=False) -> pd.DataFrame:
        """Calculates the ranking of candidates usen a given voting method.

        Parameters
        ----------
        method : {"borda", "copeland", "k-approval", "plurality"}, default="plurality"
            Method to be used for calculating the ranking.
        k : int, default=1
            Just valid for k-approval method.
        bootstrap : bool or int, default=False
            Number of bootstraps to calculate confidence interval.

        Returns
        -------
        pandas.DataFrame: 
            Ranking of candidates calculated with the method defined.

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
    
    
    def __get_items(self, method="borda", ascending=False, n=1) -> pd.DataFrame:
        df = self.ranking(method=method)
        return df.sort_values("value", ascending=ascending).head(n).reset_index(drop=True)
    

    def loser(self, method = "borda", n=1) -> pd.DataFrame:
        """Returns the loser of an election based on a voting method.

        Parameters
        ----------
        method : str, default="borda"
        n : int, default=1
            Number of losers.

        See Also
        --------
        winner: some other related function
        """
        return self.__get_items(method=method, ascending=True, n=n)
    
    
    def winner(self, method="borda", n=1) -> pd.DataFrame:
        """Returns the winner of an election based on a voting method.

        See Also
        --------
        loser: some other related function
        """
        return self.__get_items(method=method, ascending=False, n=n)
        
    
    def __transform(self, data, unique_id=False) -> pd.DataFrame:
        df = data.copy()
        df["_id"] = range(df.shape[0])
        df = df.explode("rank")
        df = df.rename(columns={"rank": "candidate"})
        df["rank"] = df.groupby("_id").cumcount() + 1
        if not unique_id:
            df = df.drop(columns=["_id"])

        return df