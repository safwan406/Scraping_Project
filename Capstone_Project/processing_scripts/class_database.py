import pymongo
import pandas as pd

class Mongo():
    """ This class is used to access the MongoDB """

    def __init__(self, uri, data_base, coll):
        """ 
        This function creates a connection to the collection of Database 
        
        Args:
            uri (str): create the instance of the MongoDB client
            data_base (str): name of database to be accessed
            coll (str): name of collection within the database
        """

        __client = pymongo.MongoClient(f'mongodb://{uri}')
        __db = __client[data_base]
        self.__collection = __db[coll]

    def update(self, my_dict):
        """ a
        This function writes into the database 
        
        Args:
            my_dict (dict): dictionary to be written inside the database
        """

        exists = self.__collection.count_documents({"heading" : my_dict['heading']})
        if exists:
            print("File already exist")
        else:
            self.__collection.insert_one(my_dict)
            print('Pushed into Mongo!')


    def read(self, key, value):
        """ 
        This function searches for key and value in the database 
        
        Args:
            key (str): key of the dictionary
            value (str): value of the dictionary
        
        Return:
            df (dataframe): the searched results from the database
        """
        myQuery = {key : {"$regex": f'^{value}'}}
        cursor = self.__collection.find(myQuery)
        df = pd.DataFrame(list(cursor))
        df = df.drop(['_id', 'news', 'ICD10_Description'], axis = 1)
        return df
