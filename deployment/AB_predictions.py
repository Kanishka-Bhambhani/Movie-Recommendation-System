########################################################
#                                                      #
#                   ONE-TIME SCRIPT                    #
#    to create AB_compatible_predictions collection    #
#                                                      #
########################################################

import sys
import os
import datetime
sys.path.append('../')
print(os.getcwd())
from helper import mongoDBHelper
from tqdm import tqdm

TS = str(datetime.datetime.now().strftime("%Y%m%dT%H:%M:%S"))
MODEL_NAME = "Jenkins_" + TS
AB_COLLECTION_NAME = 'AB_compatible_predictions' 
PREDS_COLLECTION_NAME = 'predictions_backup'

AB_dbHelper = mongoDBHelper(dbName='aieng', collectionName=AB_COLLECTION_NAME)
preds_dbHelper = mongoDBHelper(dbName='aieng', collectionName=PREDS_COLLECTION_NAME)

AB_collection = AB_dbHelper.collection
PREDS_collection = preds_dbHelper.collection

TOTAL = PREDS_collection.count_documents({})

# AB_collection.drop()

for document in tqdm(PREDS_collection.find(), total=TOTAL):

      object = {'userID': '', 
            'Jenkins_model': '',
            'Jenkins_recommendations': [],
            'AB_model': '',
            'AB_recommendations': [],
            'choice': 'A'}  # when AB-testing is turned on, some users will have this set as B

      userID = document['userID']
      recommendations = document['recommendations']

      # fill the object 
      object['userID'] = userID
      object['Jenkins_model'] = MODEL_NAME
      object['Jenkins_recommendations'] = recommendations 
      # print(object)

      AB_collection.insert_one(object)