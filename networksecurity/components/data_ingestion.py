import sys 
import pandas as pd 
import os
import numpy as np
import pymongo
from dotenv import load_dotenv
from typing import List
from sklearn.model_selection import train_test_split

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)
            df.replace({'na': np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            logging.info("Exporting data into feature store")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False)
            logging.info(f"Data exported to feature store at {feature_store_file_path}")
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info("Splitting data into train and test sets")
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42
            )
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path

            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(train_file_path, index=False)
            test_set.to_csv(test_file_path, index=False)
            logging.info(f"Data split into train and test sets at {train_file_path} and {test_file_path}")

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            logging.info("Starting data ingestion process")
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            datainfestionartifact = DataIngestionArtifact(
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion process completed with artifact: {datainfestionartifact}")
            return datainfestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
