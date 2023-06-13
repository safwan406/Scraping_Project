from snakebite.client import Client
import ast
import variables
from datetime import date

class Datalake():
    """ This class is used to access Data Lake """

    def __init__(self):
        """ This function is used to create a connection with HDFS """
        
        self.__client = Client(variables.address, variables.port)
        # print(self.client.df())

    def reader(self, file):
        """ 
        This function reads from the Data Lake 
        
        Args:
            file (str): name of directory in Data Lake

        Return:
            final_data (list): all the data present inside the passed directory
        """

        try:
            path = f'/Hadoop_File/raw_zone/new_{date.today()}_{file}.txt'
            # path = f'/Hadoop_File/raw_zone/new_2023-01-25_{file}.txt'
            for data in self.__client.text([path]):
                my_data = data.decode('utf-8')
                final_data = list(ast.literal_eval(my_data))
            return final_data
        except:
            return None
