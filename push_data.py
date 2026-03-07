import pandas as pd 
import os
import pymongo
from dotenv import load_dotenv
import json
import certifi
import sys

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()


MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()

class NetWorkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def csv_to_json_converter(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
        
    def insert_data_to_mongodb(self,records,collection,database):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mogo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mogo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

if __name__ == "__main__":
    try:
        FILE_PATH = "data/phisingData.csv"
        COLLECTION = "network_security"
        DATABASE = "naveen_db"
        data_extractor = NetWorkDataExtract()
        records = data_extractor.csv_to_json_converter(file_path=FILE_PATH)
        inserted_records = data_extractor.insert_data_to_mongodb(records=records, collection=COLLECTION, database=DATABASE)
        print(f"Total {inserted_records} records inserted to MongoDB successfully!")
    except Exception as e:
        raise NetworkSecurityException(e, sys)