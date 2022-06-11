from itertools import combinations, permutations
import numpy as np
import pandas as pd
from math import floor


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
        self.df = df.copy()
        self.df_filtered = df.copy()
        self.party = "party"
        self.rank = "rank"
        self.rank_separator = ">"
        self.show_rank = True
        self.voter = "voter"
        self.voters = "voters"

    def __set_rank__(self, df, ascending=False):
        df["rank"] = df["value"].rank(
            method="min", ascending=ascending).astype(int)
        return df

    def antiplurality(self) -> pd.DataFrame:
        return self.plurality(ascending=True)

    def black(self) -> pd.DataFrame:
        """Black procedure (1958).

        Calculates winner of an election using Black procedure. First, the method calculates if there is a
        Condorcet winner. If there is a Condorcet winner, that candidate is the winner. Otherwise, the winner
        using Borda count is the winner.

        Returns
        -------
        pandas.DataFrame:
            Election's winner using Black procedure.

        References
        ----------
        Black, Duncan (1958). The theory of committees and elections. Cambridge: University Press.
        """
        r = self.condorcet(weak=False)
        return r if r.shape[0] > 0 else self.winner(method="borda")

    def borda(self, rmv=[], score="original") -> pd.DataFrame:
        """Borda Count (1784).

        The Borda count is a voting method to rank candidates.
        In an election, each voter gives a ranked-ordered list of their preferences.
        Then, it assigns the lowest score to the lowest-ranked candidate, increasing
        the score assigned until the candidate ranks first. The winner is the candidate with the most points.

        The original version proposed by Borda for an election of n candidates, assigns `n - 1`
        points to the candidate in the first place, `n - 2` to the candidate in the second place,
        and so on, until assigning 0 to the lowest-ranked candidate.

        Parameters
        ----------
        score: {"original", "score_n", "dowdall"}, default="original"
            Method to calculate Borda score.

        Returns
        -------
        pandas.DataFrame:
            Election results using Borda Count.

        References
        ----------
        Borda, J. D. (1784). Mémoire sur les élections au scrutin. Histoire de l'Academie
        Royale des Sciences pour 1781 (Paris, 1784).
        """
        df = self.df_filtered.copy()
        candidate = self.candidate
        rank = self.rank
        voters = self.voters
        plural_voters = voters in list(df)

        # if plural_voters:
        df = self.__transform(df, rmv=rmv)
        N = len(df[candidate].unique())

        if score == "dowdall":
            df["value"] = 1 / df[rank]

        elif score == "score_n":
            df["value"] = N - df[rank] - 1

        else:
            df["value"] = N - df[rank]

        if plural_voters:
            df["value"] *= df[voters].astype(int)

        tmp = df.groupby(candidate).agg(
            {"value": "sum"}).reset_index().sort_values("value", ascending=False)
        if self.show_rank:
            tmp = self.__set_rank__(tmp)
        return tmp

    # def bootstraping(self, iter=1000) -> pd.DataFrame:
    #     return

    def compare_methods(self, rules=["borda", "copeland", "plurality"]) -> pd.DataFrame:
        """Compares the ranking given to a candidate in different aggregation methods.

        Parameters
        ----------
        rules : list of {"borda", "k-approval", "copeland", "plurality"}, optional:
            Methods to be compared. Values accepted are borda, k-approval, copeland, and plurality.

        Returns
        -------
        pandas.DataFrame:
            DataFrame with a comparison of the methods defined. The first column represents the candidate, and the following ones represent each method being compared.
        """
        output = pd.DataFrame()
        candidate = self.candidate

        for rule in rules:
            r = self.ranking(method=rule, k=1)
            r = r.rename(columns={"rank": rule})
            r = r[[candidate, rule]]
            output = r.copy() if output.shape[0] == 0 else pd.merge(
                output, r, on=candidate)

        return output

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

    def condorcet(self, weak=True):
        """Condorcet winner (1785).

        A Condorcet winner is the candidate who wins 100% of 1v1 elections regarding all
        the other candidates running in the same election (under a plurality rule).

        A weak Condorcet winner does not need to satisfy the rule of 100% of victories.

        Parameters
        ----------
        weak: bool, default=True
            If the value is `true`, returns a weak Condorcet winner.

        Returns
        -------
        pandas.DataFrame:
            Condorcet winner

        References
        ----------
        de Condorcet, M. (1785), Essai sur l'Application de l'Analyse à la Probabilité des Décisions Rendues à la Pluralité des Voix. Paris: L'Imprimerie Royale.

        Felsenthal, D.S., Tideman, N. Weak Condorcet winner(s) revisited. Public Choice 160, 313-326 (2014). https://doi.org/10.1007/s11127-014-0180-4

        """
        df = self.df_filtered.copy()
        candidate = self.candidate

        m = self.copeland_matrix()

        tmp = pd.DataFrame([(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=1)))],
                           columns=[candidate, "value"]).sort_values("value", ascending=False)

        if weak:
            return tmp.head(1)
        else:
            v = list(tmp["value"].values)
            return pd.DataFrame([]) if v[0] < 1 else tmp.head(1)

    def copeland_matrix(self, n_votes=False):
        df = self.df_filtered.copy()
        output = []

        candidate = self.candidate
        rank = self.rank
        voter = self.voter
        voters = self.voters
        rank_separator = self.rank_separator

        cols = ["_winner", "_loser"]

        def __transform(data, unique_id=False) -> pd.DataFrame:
            df = data.copy()
            df["_id"] = range(df.shape[0])
            df[rank] = df[rank].str.split(rank_separator)
            df = df.explode("rank")
            df = df.rename(columns={"rank": "candidate"})
            df[rank] = df.groupby("_id").cumcount() + 1
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

        if n_votes:
            return m

        r = m + m.T
        m = m / r

        m = np.where(m > 0.5, 1, np.where(m == 0.5, 0.5, 0))
        m = pd.DataFrame(m, index=unique_candidates, columns=unique_candidates)
        m = m.reindex(unique_candidates, axis=0)
        m = m.reindex(unique_candidates, axis=1)
        m = m.astype(float)
        np.fill_diagonal(m.values, np.nan)

        return m

    def copeland(self) -> pd.DataFrame:
        """Copeland voting method (1951).

        Each voter ranks candidates by preference. Next, we sort candidates by the
        number of times they beat another candidate in a pairwise comparison.
        The top-1 on Copeland's method is considered a weak Condorcet winner.
        Likewise, if in an election of `n` candidates, a candidate beats `n - 1`
        candidates in pairwise comparison scenarios, it is also considered a Condorcet winner.

        Returns
        -------
        pandas.DataFrame:
            Election results using Copeland method.

        References
        ----------
        Copeland, A.H. (1951). A “reasonable” social welfare function, mimeographed. In: Seminar on applications of mathematics to the social sciences. Ann Arbor: Department of Mathematics, University of Michigan.

        """
        df = self.df_filtered.copy()
        candidate = self.candidate

        m = self.copeland_matrix()

        tmp = pd.DataFrame([(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=1)))],
                           columns=[candidate, "value"]).sort_values("value", ascending=False)
        if self.show_rank:
            tmp = self.__set_rank__(tmp)

        return tmp

    def cumulative(self) -> pd.DataFrame:
        """Cumulative Voting.

        Calculates the cumulative score of each candidate.

        Returns
        -------
        pandas.DataFrame:
            Election results using Cumulative Voting
        """
        candidate = self.candidate
        rank = self.rank
        votes = self.votes
        df = self.df_filtered.copy()
        tmp = df.groupby(candidate).agg({votes: "sum"}).reset_index().rename(
            columns={votes: "value"}).sort_values("value", ascending=False)
        if self.show_rank:
            tmp = self.__set_rank__(tmp)

        return tmp

    def dowdall(self) -> pd.DataFrame:
        """Dowdall voting method (1971).

        Dowdall is an alternative to Borda count, devised by Nauru's Secretary
        of Justice in 1971. As in Borda, each voter gives a ranking of candidates.
        The first candidate gets 1 point, the 2nd candidate 1/2 points, and so on
        until the candidate ranked in the n position receives 1/n points.

        Returns
        -------
        pandas.DataFrame:
            a ranking of candidates using Dowdall.

        References
        ----------
        Fraenkel, Jon; Grofman, Bernard (3 April 2014). "The Borda Count and its real-world alternatives: Comparing scoring rules in Nauru and Slovenia". Australian Journal of Political Science. 49 (2): 186-205. doi:10.1080/10361146.2014.900530
        """
        return self.borda(score="dowdall")

    def dhondt(self, seats=1) -> pd.DataFrame:
        """D'Hondt (or Jefferson) method.

        Calculates the number of elected candidates of each party using the D'Hondt (or Jefferson) method.

        Parameters
        ----------
        seats : int, default=1, optional:
            Number of seats to be assigned in the election.

        Returns
        -------
        pandas.DataFrame:
            Summary with the seats of each party.
        """
        df = self.df_filtered.copy()
        party = self.party
        output = []
        for __party, df_tmp in df.groupby(party):
            votes = df_tmp.votes.values[0]
            for i in range(seats):
                output.append({party: __party, "quot": votes / (i + 1)})

        tmp = pd.DataFrame(output).sort_values("quot", ascending=False)
        return tmp.head(seats).groupby(party).count().reset_index().rename(columns={"quot": "seats"})

    def hare(self) -> pd.DataFrame:
        """Hare Rule (also called as Instant Runoff IRV, Ranked-Choice Voting, and Alternative Vote)

        Calculates the winner of an election. In each iteration,
        removes the candidate with the lowest score in a plurality rule,
        until to have a majority winner.

        Returns
        -------
        pandas.DataFrame:
            The election's winner using IRV.
        """
        df = self.df_filtered.copy()
        candidate = self.candidate
        rank = self.rank
        voters = self.voters

        # if voters in list(df):
        df = self.__transform(df, unique_id=True)

        def __plurality(df):
            df = df[df["rank"] == 1].copy()
            df["value"] = 1
            if "voters" in list(df):
                df["value"] *= df["voters"].astype(int)

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
            tmp = tmp.sort_values(
                "value", ascending=False).reset_index(drop=True)

        return tmp.head(1)

    def k_approval(self, k=1) -> pd.DataFrame:
        """k-Approval voting method.

        The method gives 1 if the candidate is ranked over or equal to k. Otherwise, the value given is 0.

        Parameters
        ----------
        k (int, default=1, optional):
            Threshold to score candidates with a value of 1.

        Returns
        -------
        pandas.DataFrame:
            Election results using the k-approval method.

        References
        ----------

        """
        df = self.df_filtered.copy()

        candidate = self.candidate
        rank = self.rank
        voters = self.voters
        plural_voters = voters in list(df)

        # if plural_voters:
        df = self.__transform(df)

        df["value"] = df[rank] <= k
        if plural_voters:
            df["value"] *= df[voters].astype(int)

        tmp = df.groupby(candidate).agg(
            {"value": "sum"}).reset_index().sort_values("value", ascending=False)
        if self.show_rank:
            tmp = self.__set_rank__(tmp)

        return tmp

    def kemeny_young(self, score_matrix=False):
        """Kemeny-Young method.

        The Kemeny-Young method is a voting method that uses preferential ballots
        and pairwise comparison to identify the most popular candidates in an election.

        Parameters
        ----------
        score_matrix : bool, default = False
            If the value is `true`, returns the score matrix.

        Returns
        -------
        pandas.DataFrame:
            Election results using Kemeny-Young method.

        References
        ----------
        John Kemeny, "Mathematics without numbers", Daedalus 88 (1959), pp. 577-591.

        H. P. Young, "Optimal ranking and choice from pairwise comparisons", in Information pooling and group decision making edited by B. Grofman and G. Owen (1986), JAI Press, pp. 113-122.

        H. P. Young and A. Levenglick, "A Consistent Extension of Condorcet's Election Principle", SIAM Journal on Applied Mathematics 35, no. 2 (1978), pp. 285-300.
        """
        m = self.copeland_matrix(n_votes=True)
        candidate = self.candidate
        rank = self.rank

        output = []
        for permutation in permutations(list(m)):
            score = 0
            for items in combinations(permutation, 2):
                i_winner, i_loser = items
                value = m.loc[i_winner, i_loser]
                score += value
            output.append([list(permutation), score])

        tmp = pd.DataFrame(output, columns=[rank, "value"]).sort_values(
            "value", ascending=False).reset_index(drop=True)

        if score_matrix:
            return tmp

        tmp_r = pd.DataFrame()
        tmp_r[candidate] = tmp.loc[0, "rank"]
        tmp_r[rank] = range(1, tmp_r.shape[0] + 1)

        if self.show_rank:
            tmp_r = self.__set_rank__(tmp_r)

        return tmp_r

    def minimax(self, method="winning_votes"):
        candidate = self.candidate
        d = self.copeland_matrix(n_votes=True)

        e = d / (d + d.T)

        if method in ["winning_votes", "pairwise_opposition"]:
            tmp = (1 - e).max(axis=1).to_frame(name="value")
            tmp = tmp.reset_index().rename(columns={"_winner": candidate})
            if method == "winning_votes":
                tmp.loc[tmp["value"] < 0.5, "value"] = 0

        elif method == "margins":
            tmp = (-1 * (e.T - e).min(axis=0)).to_frame(name="value")
            tmp = tmp.reset_index().rename(columns={"_winner": candidate})

        tmp = tmp.sort_values("value", ascending=True)
        tmp = tmp.reset_index(drop=True)

        return tmp.head(1)

    def nanson(self):
        return self.nanson_baldwin(method="nanson")

    def baldwin(self):
        return self.nanson_baldwin(method="baldwin")

    def nanson_baldwin(self, method="nanson") -> pd.DataFrame:
        candidate = self.candidate

        rmv = []
        tmp = self.borda(rmv=rmv)

        while tmp.shape[0] > 1:
            mean = tmp["value"].mean()
            if method == "baldwin":
                rmv += list(tmp.tail(1)[candidate].unique())
            elif method == "nanson":
                rmv += list(tmp[tmp["value"] < mean][candidate].unique())
            tmp = self.borda(rmv=rmv)

        return tmp

    def negative(self) -> pd.DataFrame:
        """Negative Voting.

        Calculates the score of each candidate using Negative Voting.

        Returns
        -------
        pandas.DataFrame: 
            Election results using Negative Voting.

        """
        candidate = self.candidate
        rank = self.rank
        votes = self.votes
        df = self.df_filtered.copy()

        tmp = df.groupby(candidate).agg({votes: "sum"}).reset_index().rename(
            columns={votes: "value"}).sort_values("value", ascending=False)
        if self.show_rank:
            tmp = self.__set_rank__(tmp)

        return tmp

    def plurality(self, ascending=False):
        """Plurality Rule.

        Each voter selects one candidate (or none if voters can abstain), and the candidate(s) with the most votes win.

        Returns
        -------
        pandas.DataFrame:
            Election results using Plurality Rule.
        """
        df = self.df_filtered.copy()

        candidate = self.candidate
        rank = self.rank
        voters = self.voters

        # if voters in list(df):
        df = self.__transform(df)

        df = df[df[rank] == 1]
        df["value"] = 1
        if voters in list(df):
            df["value"] *= df[voters].astype(int)

        tmp = df.groupby(candidate).agg(
            {"value": "sum"}).reset_index().sort_values("value", ascending=ascending)
        if self.show_rank:
            tmp = self.__set_rank__(tmp, ascending=ascending)

        return tmp

    def quota(self, n_votes, seats, method="hare") -> int:
        if method == "hare":
            return floor(n_votes / seats)
        elif method == "imperiali":
            return round(n_votes / (seats + 2), 0)
        elif method == "droop":
            return floor(n_votes / (seats + 1)) + 1
        elif method == "hagenbach-bischoff":
            return floor(n_votes / (seats + 1))
        return 1

    def score(self) -> pd.DataFrame:
        """Score Voting. (Also called as Range Voting, Utilitarian Voting).

        In this method, voters give a score to each candidate. We average the scores, 
        and the winner is the candidate with the highest score.

        Returns
        -------
        pandas.DataFrame:
            Election results using Score Voting.

        """
        candidate = self.candidate
        rank = self.rank
        votes = self.votes
        df = self.df_filtered.copy()
        tmp = df.groupby(candidate).agg({votes: "mean"}).reset_index().rename(
            columns={votes: "value"}).sort_values("value", ascending=False)
        if self.show_rank:
            tmp = self.__set_rank__(tmp)

        return tmp

    def schulze(self):
        candidate = self.candidate

        d = self.copeland_matrix(n_votes=True)
        candidates = list(d)
        n_candidates = len(candidates)

        p = pd.DataFrame(
            np.zeros((n_candidates, n_candidates)),
            index=candidates,
            columns=candidates
        )

        for i in candidates:
            for j in candidates:
                if i != j:
                    if d[i][j] > d[j][i]:
                        p[i][j] = d[i][j]

        for i in candidates:
            for j in candidates:
                if i != j:
                    for k in candidates:
                        if i != k and j != k:
                            p[j][k] = max(p[j][k], min(p[j][i], p[i][k]))

        tmp = pd.DataFrame((p > p.T).astype(int).sum(axis=1)).reset_index()
        tmp.columns = [candidate, "value"]

        if self.show_rank:
            tmp = tmp.sort_values("value", ascending=False)
            tmp = tmp.reset_index(drop=True)
            tmp = self.__set_rank__(tmp)

        return tmp

    def smith_set(self):
        """Smith Set.

        The Smith Set, Generalized Top-Choice Assumption (GETCHA), or Top Cycle, 
        is the smallest non-empty set of candidates in an election. 
        Each member defeats every candidate outside the set in a pairwise election. 

        Returns
        -------
        list:
            Candidates that are part of the Smith Set.
        """

        output = []
        m = self.copeland_matrix()
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
