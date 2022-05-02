import pandas as pd
from pymongo import MongoClient


class mongoDBHelper():
    def __init__(self, dbName = None, collectionName = None):
        """
        Setup the connection
        """
        self.client = MongoClient('mongodb://128.2.205.130:27017/')
        self.collection = None

        if dbName is not None:
            self.db = self.client[dbName]
        
        if dbName is not None and collectionName is not None:
            self.collection = self.db[collectionName]
        
        return None

    def set_db(self, db_name = 'aieng'):
        """
        Connect to the database.
        """
        self.db = self.client[db_name]

    def set_collection(self, collection_name):
        """
        Get the collection from the database.
        """
        self.collection = self.db[collection_name]

    def get_collection_data(self):
        """
        Get the data from the collection.
        """
        data = self.collection.find()
        return data

    def convert_to_df(self, data):
        """
        Convert the data to a pandas dataframe.
        """
        df = pd.DataFrame(list(data))
        return df




