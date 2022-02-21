import pandas as pd


class Rating:
    def __init__(self, df):
        self.candidate = "candidate"
        self.df = df
        self.rank = "rank"
        self.voter = "voter"


    def borda(self):
        """
        Calculates Borda Count
        """
        df = self.df.copy()
        candidate = self.candidate
        N = len(df[candidate].unique())
        df["value"] = N - df[self.rank]
        return df.groupby(candidate).agg({"value": "sum"}).reset_index()


    def plurality(self):
        """
        Each voter selects one candidate (or none if voters can abstain), and the candidate(s) with the most votes win.
        """
        df = self.df.copy()
        candidate = self.candidate
        return df[df["rank"] == 1].groupby(candidate).agg({"rank": "count"}).reset_index().rename(columns={"rank": "value"})