from itertools import combinations, permutations
import numpy as np
import pandas as pd


class Voting:
    """Voting.

    The class `Voting` defines rules to make collective decisions.
    It includes methods to calculate candidates' ranking and some
    axiomatic properties in social choice theory.

    Attributes
    ----------
    candidate: str, default="candidate"
        Candidates' unique identifier.
    party: str, default="party"
        Party's unique identifier. (Attribute used for proportional methods).
    rank: str, default="rank"
        Ranking of candidates selected by a voter.
    show_rank: bool, default=True
        If the value is `true`, the ranking methods defined in `Voting`
        will include a column with the ranking of each candidate.
    voter: str, default="voter"
        Voter's unique identifier.
    voters: str, default="voters"
        If `voter` is not defined, and each row represents more than one voter,
        it includes the number of voters that selected the same ranking of candidates.

    """

    def __init__(self, data):
        # If data is not a DataFrame, converts it data into a DataFrame
        df = data.copy() if isinstance(data, pd.DataFrame) else pd.DataFrame(data)

        self.candidate = "candidate"
        self.candidates = "candidates"
        self.candidates_separator = ","
        self.df = df.copy()
        self.df_filtered = df.copy()
        self.party = "party"
        self.rank = "rank"
        self.rank_separator = ">"
        self.score = "score"
        self.show_rank = True
        self.voter = "voter"
        self.voters = "voters"

    def completeness(self) -> bool:
        """Completeness of data.

        Verifies if each voter sets a ranking of candidates.
        Required in voting methods that need a ranking of candidates provided by each voter.

        Returns
        -------
        bool:
            Boolean variable to indicate if the data is complete.
        """
        df = self.df_filtered.copy()

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

    def ranking(self, method="plurality", **args) -> pd.DataFrame:
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
            "k-approval": self.k_approval(**args),
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

    def loser(self, method="borda", n=1) -> pd.DataFrame:
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

        Parameters
        ----------
        method : str, default="borda"
        n : int, default=1
            Number of losers.

        See Also
        --------
        loser: some other related function
        """
        return self.__get_items(method=method, ascending=False, n=n)

    def __transform(self, data, rmv=[], unique_id=False) -> pd.DataFrame:
        df = data.copy()
        df["_id"] = range(df.shape[0])
        df["rank"] = df["rank"].str.split(self.rank_separator)
        df = df.explode("rank")
        df = df.rename(columns={"rank": "candidate"})

        if len(rmv) > 0:
            df = df[~df["candidate"].isin(rmv)].copy()

        df["rank"] = df.groupby("_id").cumcount() + 1
        if not unique_id:
            df = df.drop(columns=["_id"])

        return df
