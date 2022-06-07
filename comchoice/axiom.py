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

    def faithfulness():
        """
            Faithfulness: There is only one winner when considering just one voter.

        Returns
        -------
        bool:
            Boolean variable to indicate if the data is complete.
        """

        return False
        
    def reinforcement():
        """
            Reinforcement: a candidate that it is selected by two different voters 
            must also be the one voted by their votes together.  

        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """
        return False
        
    def cancellation():
        """
            Cancellation: all tied alternatives in the 
            top-ranked position will win.
        
        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """
        return False
        
    def pareto():
        """
            Pareto: Dominated alternatives can not win.
        
        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """

        if Axiom.condocert(data):
            return False         


        return False

    def condocert(data):
        """
            Condocert: the candidate that wins from all other candidates in
             any pairwise comparision will be the winner. 
        
        Returns
        -------
        bool:
            Boolean variable to indicate if the data is complete.
        """
        
        return False

    def weak_condocert(data):
        """
            Condocert: the candidate that wins from all other candidates in
             any pairwise comparision will be the winner. 
        
        Returns
        -------
        bool:
            Boolean variable to indicate if the data is complete.
        """
        
        return False
        
    def neutrality():
        """
            Neutrality: all alternatives must have equal weight.
        
        Returns
        -------
        bool: 
            Boolean variable to indicate if the data is complete.
        """
        return False 

    