import pandas as pd
import re
import time

class NDC():
    """ This class is used to extract NDC code """
    
    def __init__(self, file):
        """ 
        This function creates a dataframe for prescription codes
        
        Args:
            file (str): name of csv file for prescription codes
        """

        self.__df = pd.read_csv(file)
        self.__df['Product Name'] = self.__df['Product Name'].str.lower()

    def classifier_for_code(self, content):
        """ 
        This function matches the name of medicines and returns its NDC
        
        Args:
            content (str): the scraped article

        Return:
            codes (list): list of NDC
            medicine (list): list of matched string for prescription
        """

        try:
            medicine = set()
            codes = set()
            startTime = time.time()
            for productName, productCode in zip(self.__df['Product Name'], self.__df['Code']):
                words = (re.findall(r'\b%s\b'%productName, content))
                words = (list(dict.fromkeys(words)))
                if (len(words) > 0):
                    medicine.add(words[0])
                    codes.add(productCode)
            stopTime = time.time()
            elapsedTime = stopTime - startTime
            print(f'Time to match is {elapsedTime} sec')
            
            return list(codes), list(medicine)
        
        except:
            print('empty list')
            return [], []
