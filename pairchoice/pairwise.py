import numpy as np
import pandas as pd
import tqdm

from .__data_cleaning import _create_card_id

class Pairwise:
    """Class Pairwise.

    Attributes
    ----------
    candidate: str
        Column name that includes the candidates.
    
    """
    def __init__(self, df):
        self.candidate = "candidate"
        self.df = df
        self.option_a = "option_a"
        self.option_b = "option_b"
        self.selected = "selected"
        self.value = "value"
        self.voter = "voter"


    def ahp(self):
        """
        Calculates a ranking of candidates using Automatic Hierarchy Process (AHP)
        Reference: Saaty 1980
        """
        candidate = self.candidate
        df = self.df.copy()
        voter = self.voter

        dd = df.groupby(["option_source", "option_target"]).agg({voter: "count"}).reset_index()

        a = dd.pivot(index="option_target", columns="option_source", values=voter)
        b = np.divide(a, a.T)
        np.fill_diagonal(b.values, 1)
        c = b / b.sum()
        weight = [1/c.shape[0] for i in range(c.shape[0])]

        tmp = pd.DataFrame(np.sum(np.multiply(c, weight), axis=1)).reset_index().rename(columns={"option_target": candidate, 0: "value"})

        return tmp


    def copeland(self):
        """
        Calculates a ranking sorting candidates based on the Condorcet winner.
        """
        candidate = self.candidate
        df = self.df.copy()
        m = self.matrix_pairs(df) > 0.5
        m = m.astype(float)
        np.fill_diagonal(m.values, np.nan)

        return pd.DataFrame(
            [(a, b) for a, b in list(zip(list(m), np.nanmean(m, axis=0)))], 
            columns=[candidate, "value"]
        )


    def matrix_pairs(self, df):
        voter = self.voter
        dd = df.groupby(["option_source", "option_target"]).agg({voter: "count"}).reset_index()
        m = dd.pivot(index="option_source", columns="option_target",
                    values=voter).fillna(0)
        ids = set(df["option_source"]) | set(df["option_target"])
        m = m.reindex(ids)
        m = m.reindex(ids, axis=1)
        m = m.fillna(0)

        r = m + m.T
        return m / r


    def divisiveness(self) -> pd.DataFrame:
        """Calculates the level of disagreement that generates a candidate between voters.

        Returns
        -------
        pandas.DataFrame
            A set of candidates and their respective divisiveness

        References
        ----------
        Navarrete & Hidalgo (forthcoming)
        """
        df = self.df.copy()
        df = df[df[self.selected] != 0].copy()

        candidate = self.candidate
        option_a = self.option_a
        option_b = self.option_b
        selected = self.selected
        value = self.value
        voter = self.voter

        dd = df.groupby(["card_id", selected, voter]).agg({"id": "count"})
        _data = df.copy().set_index(voter)
        
        _ = self.win_rate

        def _f(idx, df_select):
            card_id = idx[0]
            s = idx[1]

            users = [item[2] for item in df_select.index.to_numpy()]
            
            data_temp = _data.loc[users]

            r_tmp = _(data_temp.reset_index()).dropna()
            r_tmp["card_id"] = card_id
            r_tmp[selected] = s

            del data_temp, users

            return r_tmp

        tmp_list = []

        _data_tmp = dd.groupby(level=[0, 1])

        for idx, df_select in tqdm.tqdm(_data_tmp, position=0, leave=True):
            tmp_list.append(_f(idx, df_select))

        tmp = pd.concat(tmp_list, ignore_index=True)

        tmp[[f"{option_a}_sorted", f"{option_b}_sorted"]] = tmp["card_id"].str.split("_", expand=True)
        tmp["group"] = tmp[f"{option_a}_sorted"].astype(str) == tmp[selected].astype(str)
        tmp["group"] = tmp["group"].replace({True: "A", False: "B"})
        
        tmp_a = tmp[tmp["group"] == "A"]
        tmp_b = tmp[tmp["group"] == "B"]
        
        tmp_dv = pd.merge(tmp_a, tmp_b, on=["card_id", candidate, f"{option_a}_sorted", f"{option_b}_sorted"])
        tmp_dv = tmp_dv[[candidate, "card_id", "value_x", "value_y", f"{selected}_x", f"{selected}_y"]]
        tmp_dv["value"] = abs(tmp_dv["value_x"] - tmp_dv["value_y"])

        tmp_frag_a = tmp_dv[[candidate, f"{selected}_x", "value"]].rename(columns={f"{selected}_x": "selected"})
        tmp_frag_b = tmp_dv[[candidate, f"{selected}_y", "value"]].rename(columns={f"{selected}_y": "selected"})
        tmp_frag_c = pd.concat([tmp_frag_a, tmp_frag_b])
        tmp_frag_c = tmp_frag_c[tmp_frag_c[candidate] == tmp_frag_c["selected"]]
        tmp_frag_c = tmp_frag_c.groupby(candidate).agg({"value": "mean"}).reset_index()

        return tmp_frag_c


    def elo(self, rating=400, K=10):
        """
        Calculates a ranking of candidates using Elo rating.
        """
        df = self.df.copy()

        ELO_RATING = {i: rating for i in set(df["option_a_sorted"]) | set(df["option_b_sorted"])}

        for option_a, option_b, selected in list(zip(df["option_a_sorted"], df["option_b_sorted"], df["option_selected"])):
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

        tmp = pd.DataFrame(ELO_RATING.items(), columns=[self.candidate, "value"])

        return tmp


    def transform(self):
        """
        Transforms the data defined by the user into a valid pairchoice data set. 
        That is, it includes columns needed to run aggregation methods and other analysis defined in the class.
        """
        df = self.df
        df = _create_card_id(df)
        df["id"] = range(0, df.shape[0])
        self.df = df


    def to_pairwise(self):
        """
        Converts a rating-based data set into a pairwise comparison data set.
        """
        df = self.df
        
        candidate = self.candidate
        option_a = self.option_a
        option_b = self.option_b
        selected = self.selected
        value = self.value
        voter = self.voter
        
        output = []
        for user_id, df_tmp in tqdm.tqdm(df.groupby(voter), position=0, leave=True):
            tmp = pd.merge(df_tmp, df_tmp, on=voter, how="outer")
            tmp = tmp[tmp[f"{candidate}_x"] != tmp[f"{candidate}_y"]]
            tmp = tmp[tmp[f"{candidate}_x"] > tmp[f"{candidate}_y"]]
            output.append(tmp)
            del tmp
            
        tmp = pd.concat(output)
        tmp = tmp.rename(columns={f"{candidate}_x": option_a, f"{candidate}_y": option_b})
        tmp["selected"] = np.where(
            tmp[f"{value}_x"] == tmp[f"{value}_y"], 0, 
            np.where(tmp[f"{value}_x"] > tmp[f"{value}_y"], tmp[option_a], tmp[option_b])
        )

        self.df = tmp[[voter, option_a, option_b, selected]]


    def win_rate(self, data=None):
        """
        Calculates the fraction of times a proposal is selected with respect to the total of its occurrences.
        """
        df = data.copy() if isinstance(data, pd.DataFrame) else self.df.copy()
        df = df[df[self.selected] != 0]
        candidate = self.candidate
        voter = self.voter

        dd = df.groupby(["option_source", "option_target"]).agg({voter: "count"}).reset_index()
        m = dd.pivot(index="option_source", columns="option_target", values=voter).fillna(0)
        ids = set(df["option_source"]) | set(df["option_target"])
        m = m.reindex(ids)
        m = m.reindex(ids, axis=1)
        m = m.fillna(0)

        r = m + m.T
        values = m.sum() / r.sum()

        return pd.DataFrame(values).reset_index().rename(columns={"option_target": candidate, 0: "value"})