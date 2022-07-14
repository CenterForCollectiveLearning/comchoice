import pandas as pd


class Axiom:
    """Axiom.

    The class `Axiom` checks whether the properties of the voting system,
    data, and individual and collective rankings holds true. 

    """

    def compute_ranking(data, n_candidates, columns=['option_source', 'option_target']):
        ranking = ((data[columns[0]].value_counts().reindex(range(1, n_candidates+1), fill_value=0)*-1)
                   +
                   (data[columns[1]].value_counts().reindex(range(1, n_candidates+1), fill_value=0)*(n_candidates-1))).reset_index()
        ranking[1] = ranking[0].rank(
            ascending=False, method='first').astype(int)
        return list(ranking.sort_values(by='index', ascending=True)[1].values), list(ranking.sort_values(by='index', ascending=True)[0].values)

    def compute_ranking_ties(data, n_candidates, columns=['option_source', 'option_target']):
        ranking = ((data[columns[0]].value_counts().reindex(range(1, n_candidates+1), fill_value=0)*-1)
                   +
                   (data[columns[1]].value_counts().reindex(range(1, n_candidates+1), fill_value=0)*(n_candidates-1))).reset_index()
        ranking[1] = ranking[0].rank(
            ascending=False, method='average').astype(int)
        return list(ranking.sort_values(by='index', ascending=True)[1].values), list(ranking.sort_values(by='index', ascending=True)[0].values)

    def sort_option_columns(data, columns=["option_a", "option_b", "selected"]):
        data['option_a_sorted'] = data.apply(
            lambda x: x['option_a'] if x['option_a'] < x['option_b'] else x['option_b'], axis=1)
        data['option_b_sorted'] = data.apply(
            lambda x: x['option_b'] if x['option_a'] < x['option_b'] else x['option_a'], axis=1)
        data["card_id"] = data["option_a_sorted"].apply(
            str) + "-" + data["option_b_sorted"].apply(str)
        data['option_selected'] = data.apply(
            lambda x: +1 if x['option_a_sorted'] == x['selected'] else -1, axis=1)
        return data

    def standardize_data_columns(data, columns=["option_a", "option_b", "selected"]):
        for col in columns:
            data[col] = data[col].apply(lambda x: "%.2d" % int(x))

        a = data[columns].values
        data["option_source"] = np.where(a[:, 1] == a[:, 2], a[:, 0], a[:, 1])
        data["option_target"] = np.where(a[:, 0] == a[:, 2], a[:, 0], a[:, 1])
        return data

    def reinforcement(data, user_id_col='voter', selected_col='selected'):
        """
            Reinforcement: a candidate that it is selected by different voters 
            must also be the one voted by their votes together. 
            Same of Condocert, but here you do not need to take into account the whole population.

        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """
        return Axiom.condocert(data, user_id_col='voter', selected_col='selected')
