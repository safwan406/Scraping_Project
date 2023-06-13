import pandas as pd

class ICD():
    """ This class is used to extract ICD code """

    def __init__(self, file):
        """ 
        This function creates a dataframe for diagnosis codes
        
        Args:
            file (str): name of csv file for diagnosis codes
        """

        self.__df = pd.read_csv(file, header = None)
        self.__df.columns = ['ICD10', 'Point', 'Combined', 'Des_1', 'Des_2', 'Des_3']
        self.__df['Des_3'] = self.__df['Des_3'].str.lower()

    def classifier_for_code(self, disease):
        """ 
        This function matches the name of disease and returns its ICD10 code
        
        Args:
            disease (str): name of disease

        Return:
            codes (list): list of ICD10 codes
        """
        
        try:
            # duplications can also be removed by using set too
            codes = (list((self.__df['ICD10'][self.__df['Des_3'].str.contains(disease)]).drop_duplicates()))
            return codes
        except:
            print('empty list')
            return []

    def classifier_for_description(self, disease):
        """ 
        This function matches the name of disease and returns its description of ICD10 code
        
        Args:
            disease (str): name of disease

        Return:
            descriptions (list): descriptions of ICD10 codes
        """

        try:
            descriptions = (list((self.__df['Des_1'][self.__df['Des_3'].str.contains(disease)]).drop_duplicates()))
            return descriptions
        except:
            print('empty list')
            return []