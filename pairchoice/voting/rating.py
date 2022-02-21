import pandas as pd


class Rating:
    def __init__(self, df):
        self.candidate = "candidate"
        self.df = df
        self.rank = "rank"
        self.voter = "voter"
        self.voters = "voters"


    def borda(self):
        """
        Calculates Borda Count
        """
        candidate = self.candidate
        df = self.df.copy()
        rank = self.rank
        voters = self.voters
        plural_voters = voters in list(df)

        if plural_voters:
            df = self.transform(df)
        N = len(df[candidate].unique())
        df["value"] = N - df[rank]
        if plural_voters:
            df["value"] *= df[voters]

        return df.groupby(candidate).agg({"value": "sum"}).reset_index()
    
    
    def copeland(self):
        df = self.df.copy()
        output = []

        candidate = self.candidate
        rank = self.rank
        voter = self.voter
        voters = self.voters

        cols = ["_winner", "_loser"]

        if "voters" in list(df):
            df = self.transform(df, unique_id=True)
            df = df.rename(columns={"_id": "voter"})

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

        return pd.DataFrame([(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=1)))], columns=[candidate, "value"])

    
    def plurality(self):
        """
        Each voter selects one candidate (or none if voters can abstain), and the candidate(s) with the most votes win.
        """
        df = self.df.copy()
        if "voters" in list(df):
            df = self.transform(df)
        df = df[df["rank"] == 1]
        df["value"] = 1
        if "voters" in list(df):
            df["value"] *= df["voters"]

        return df.groupby("candidate").agg({"value": "sum"}).reset_index()


    def transform(self, data, unique_id=False):
        df = data.copy()
        df["_id"] = range(df.shape[0])
        df = df.explode("rank")
        df = df.rename(columns={"rank": "candidate"})
        df["rank"] = df.groupby("_id").cumcount() + 1
        if not unique_id:
            df = df.drop(columns=["_id"])

        return df