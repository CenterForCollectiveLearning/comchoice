from math import factorial
import pandas as pd


class Axiom:
    """Axiom.

    The class `Axiom` checks whether the properties of the voting system,
    data, and individual and collective rankings holds true. 

    """

    def __init__(self):
        pass

    def calculate_number_of_combinations_for_complete_information(n_candidates, number_preferences):
        return factorial(n_candidates)/(factorial(number_preferences)*factorial(n_candidates - number_preferences))

    def compute_ranking(data, n_candidates, columns=['option_source','option_target']):
        ranking = ((data[columns[0]].value_counts().reindex(range(1,n_candidates+1), fill_value=0)*-1)\
        + \
        (data[columns[1]].value_counts().reindex(range(1,n_candidates+1), fill_value=0)*(n_candidates-1))).reset_index()
        ranking[1] = ranking[0].rank(ascending=False, method='first').astype(int)
        return list(ranking.sort_values(by='index', ascending=True)[1].values), list(ranking.sort_values(by='index', ascending=True)[0].values)

    def compute_ranking_ties(data, n_candidates, columns=['option_source','option_target']):
        ranking = ((data[columns[0]].value_counts().reindex(range(1,n_candidates+1), fill_value=0)*-1)\
        + \
        (data[columns[1]].value_counts().reindex(range(1,n_candidates+1), fill_value=0)*(n_candidates-1))).reset_index()
        ranking[1] = ranking[0].rank(ascending=False, method='average').astype(int)
        return list(ranking.sort_values(by='index', ascending=True)[1].values), list(ranking.sort_values(by='index', ascending=True)[0].values)

    def sort_option_columns(data, columns=["option_a", "option_b", "selected"]):
        data['option_a_sorted'] = data.apply(lambda x: x['option_a'] if x['option_a'] < x['option_b'] else x['option_b'], axis=1)
        data['option_b_sorted'] = data.apply(lambda x: x['option_b'] if x['option_a'] < x['option_b'] else x['option_a'], axis=1)
        data["card_id"] = data["option_a_sorted"].apply(str) +  "-" + data["option_b_sorted"].apply(str)
        data['option_selected'] = data.apply(lambda x: +1 if x['option_a_sorted']==x['selected'] else -1, axis=1)
        return data

    def standardize_data_columns(data, columns=["option_a", "option_b", "selected"]):
        for col in columns:
            data[col] = data[col].apply(lambda x: "%.2d"%int(x))

        a = data[columns].values
        data["option_source"] = np.where(a[:, 1] == a[:, 2], a[:, 0], a[:, 1])
        data["option_target"] = np.where(a[:, 0] == a[:, 2], a[:, 0], a[:, 1])
        return data

    def completeness(data, n_candidates, data_columns=['voter','option_a','option_b'], number_preferences = 2) -> bool:
        """

        Completeness: a data is complete if all candidates provided their
        pairwise preferences between all the candidates.

        Returns
        -------
        bool:
            Boolean variable to indicate if the data is complete.
        """
        
        min_num = data.drop_duplicates(subset=data_columns).groupby(data_columns[0])[data_columns[1]].count().min()
        expected_num = Axiom.calculate_number_of_combinations_for_complete_information(n_candidates,number_preferences)
        return min_num == expected_num

    def incompleteness(data, n_candidates, data_columns=['voter','option_a','option_b'], number_preferences = 2) -> bool:
        """
        Incompleteness: a data is incomplete if any candidate does not provided their
        entire pairwise preferences between all the candidates.
        
        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """
        return not Axiom.completeness(data, n_candidates, data_columns, number_preferences)

    def faithfulness(data, options, selected_col='selected'):
        """
            Faithfulness: There is only one winner when considering just one voter.
            There is no absent vote. Each vote would elect someone.

        Returns
        -------
        bool:
            Boolean variable to indicate if the data is complete.
        """

        if len(data[~data[selected_col].isin(options)]) == 0:
            return True

        return False
        
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
        
    def cancellation(data, user_id_col='voter', selected_col='selected'):
        """
            Cancellation: all tied alternatives in the 
            top-ranked position will win.
        
        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """
        
        aux = data.groupby(user_id_col)[selected_col].value_counts(normalize=True)
        n_unique_winners = aux.nlargest(1, keep='all').reset_index(name='perc')[selected_col].nunique()
        if n_unique_winners > 1:
            return True

        return False
        
    def pareto(data, user_id_col='voter', selected_col='selected'):
        """
            Pareto: Dominated alternatives can not win.
            There are multiple winners. 
            Other utility function should be used to find a unique winner.
        
        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """

        if Axiom.condocert(data):
            return False       

        aux = data.groupby(user_id_col)[selected_col].value_counts(normalize=True)
        n_unique_winners = aux.nlargest(1, keep='all').reset_index(name='perc')[selected_col].nunique()
        if n_unique_winners > 1:
            return True

        return False

    def condocert(data, user_id_col='voter', selected_col='selected'):
        """
            Condocert: the candidate that wins from all other candidates in
             any pairwise comparision will be the winner. 
        
        Returns
        -------
        bool:
            Boolean variable to indicate if the data is complete.
        """
        
        aux = data.groupby(user_id_col)[selected_col].value_counts(normalize=True)
        overall_winner = aux.nlargest(1).reset_index(name='perc')[selected_col].values[0]
        aux = aux.reset_index(name='perc')
        aux = aux.merge(aux.groupby(user_id_col)\
            .apply(lambda x: x['perc'].nlargest(1)).reset_index(name='perc'), \
                on=[user_id_col,'perc'])
        if aux[selected_col].nunique() == 1 and overall_winner in aux[selected_col].unique():
            return True

        return False

    def weak_condocert(data, user_id_col='voter', selected_col='selected'):
        """
            Weak condocert: the candidate that wins from all other candidates in
             most pairwise comparisions will be the winner. It will be False, 
             if there is a strong Condocert winner or there are tied/multiple winners.
        
        Returns
        -------
        bool:
            Boolean variable to indicate if the data is complete.
        """
        if Axiom.condocert(data, user_id_col='voter', selected_col='selected'):
            return False
        
        aux = data.groupby(user_id_col)[selected_col].value_counts(normalize=True)
        n_unique_winners = aux.nlargest(1, keep='all').reset_index(name='perc')[selected_col].nunique()
        if n_unique_winners == 1:
            return True

        return False
        
    def neutrality(data, data_columns=['voter','option_a','option_b']):
        """
            Neutrality: all alternatives must have equal weight.
            No duplicated votes.
        
        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """
        return (data.groupby(data_columns[1:])[data_columns[0]].count()\
                    ==\
                    data.groupby(data_columns[1:])[data_columns[0]].nunique())\
                        .all()


    