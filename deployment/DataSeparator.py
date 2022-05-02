import datetime
import sys
import os
import os.path as osp

import pip
sys.path.append(os.getcwd())
from helper import mongoDBHelper
import pymongo
import pickle

class DataSeperator():
    def __init__(self, dbName='aieng', collectionName='AB_ratings'):
        self.dbHelper = mongoDBHelper(dbName, collectionName)
        # the provenance collection
        self.provenance = mongoDBHelper(dbName, 'provenance')
        
    def getData(self):
        try:
            # self.maxCount = 5000
            # self.data = self.dbHelper.collection.find().sort('ts', pymongo.ASCENDING, )
            pipeline = [{"$match": {}},
                {"$sort": {"ts": pymongo.ASCENDING}}]
            # allow disk use so that it won't crash when sorting based on 'ts'
            self.data = self.dbHelper.collection.aggregate(pipeline=pipeline, allowDiskUse=True)

            self.data_count = self.dbHelper.collection.count_documents({})

            # Test data is fixed at 10,000, rest of the data will be training data
            self.test_count = 10000
            self.train_count = self.data_count - self.test_count
            # if the training data is less than test data, use the ratio
            if (self.train_count < self.test_count):
                self.train_test_split_ratio = 0.025
                self.train_count = int((1-self.train_test_split_ratio)*self.data_count)
                self.test_count = self.data_count - self.train_count

            self.train_data = {}
            self.test_data = {}
            return True
        except:
            return False

    def processData(self):
        # get train_data and test_data
        train_start_ts_record = False
        test_start_ts_record = False
        self.train_start_ts, self.train_end_ts = -1, -1
        self.test_start_ts, self.test_end_ts = -1, -1
        counter = 0
        for data in self.data:
            try:
                if counter < self.train_count:
                    if train_start_ts_record == False:
                        train_start_ts_record = True
                        self.train_start_ts = data['ts']
                    self.train_end_ts = data['ts']
                    self.train_data[(int(data['userID']), data['movieID'])] = int(data['rating'])
                else:
                    if test_start_ts_record == False:
                        test_start_ts_record = True
                        self.test_start_ts = data['ts']
                    self.test_end_ts = data['ts']
                    if data['userID'] in self.test_data:
                        self.test_data[int(data['userID'])].append(data['movieID'])
                    else:
                        self.test_data[int(data['userID'])] = [data['movieID']]
            except:
                print(data)
                pass
            finally:
                counter += 1
        return True

    def saveData(self, save_provenance = False):
        print(f"Saving train_data: {len(self.train_data)}")
        print(f"Saving test_data: {len(self.test_data)}")

        try:
            with open('train.pkl', 'wb') as file:
                pickle.dump(self.train_data, file, pickle.HIGHEST_PROTOCOL)

            with open('test.pkl', 'wb') as file:
                pickle.dump(self.test_data, file, pickle.HIGHEST_PROTOCOL)
            
            if save_provenance:
                ts = datetime.datetime.now()
                self.provenance.collection.insert_one({
                    "modelID": "Jenkins_" + str(ts.strftime("%Y%m%dT%H:%M:%S")),
                    "train_start_ts": self.train_start_ts,
                    "train_end_ts": self.train_end_ts,
                    "test_start_ts": self.test_start_ts,
                    "test_end_ts": self.test_end_ts,
                    "ts": ts,
                    'hit_metric': 0.0
                })

            return True
        except:
            return False

if __name__ == '__main__':
    dataSeperator = DataSeperator()
    dataSeperator.getData()
    dataSeperator.processData()
    dataSeperator.saveData(save_provenance = True)