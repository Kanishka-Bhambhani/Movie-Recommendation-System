from fastapi import FastAPI, Response
import sys
import os
from datetime import datetime
import uvicorn

sys.path.append(os.path.dirname(os.getcwd()))
import helper as hlp

AB_COLLECTION_NAME = 'AB_compatible_predictions'

app = FastAPI()
predictions_db = hlp.mongoDBHelper('aieng', 'predictions')
ab_predictions_db = hlp.mongoDBHelper('aieng', AB_COLLECTION_NAME)
service_recommendations_log_db = hlp.mongoDBHelper('aieng', 'service_recommendations_log')

BASE_RECOMMENDATIONS = ['the+wrong+trousers+1993', 'a+close+shave+1995', 'viy+1967', 'alaskaland+2013', 'one+flew+over+the+cuckoos+nest+1975', 
                'casablanca+1942', 'lawrence+of+arabia+1962', 'cool+hand+luke+1967', 'crouching+tiger_+hidden+dragon+2000', 
                'shrek+2001', 'lethal+weapon+2+1989', 'the+untouchables+1987', 'one+flew+over+the+cuckoos+nest+1975', 
                'the+dark+knight+2008', 'the+bridge+on+the+river+kwai+1957', 'vertigo+1958', 'american+beauty+1999', 'fargo+1996', 
                'rear+window+1954', 'citizen+kane+1941']

import requests
# try:
# refresh_ports_response = requests.get("http://17645-team12.isri.cmu.edu:7000/refresh_ports")
# except:
#     print("Could not refresh ports")

def initialise_service_recommendations_log_record():
    return {
        'userID': '',
        'recommendations': [],
        'modelID': '',
        'ts': ''
    }

def update_service_log(record, return_base = False):
    try:
        service_log = initialise_service_recommendations_log_record()
        service_log['userID'] = record['userID']
        if return_base:
            service_log['modelID'] = 'BASE'
            service_log['recommendations'] = BASE_RECOMMENDATIONS

        elif record['choice'] == 'A':
            service_log['modelID'] = record['Jenkins_model']
            service_log['recommendations'] = record['Jenkins_recommendations']
        else:
            service_log['modelID'] = record['AB_model']
            service_log['recommendations'] = record['AB_recommendations']
        
        ts = datetime.now()
        service_log['ts'] = ts

        service_recommendations_log_db.collection.insert_one(service_log)

    except Exception as e:
        print(e)


def fetch_recommendations(userID):
    try:
        data = ab_predictions_db.collection.find({"userID": userID}).hint('userID_hashed')
        for record in data:
            if record['choice'] == 'A':
                update_service_log(record)
                return record['Jenkins_recommendations']
            else:
                update_service_log(record)
                return record['AB_recommendations']

        update_service_log(record, return_base=True)
        return BASE_RECOMMENDATIONS
    except Exception as e:
        return BASE_RECOMMENDATIONS


@app.get("/")
async def root():
    return {f"message": "Hello team 12"}

@app.get("/recommend/{user_id}")
async def recommend(user_id: int):
    # results = getRecommendation(str(user_id))
    results = fetch_recommendations(str(user_id))
    return Response(','.join(results))

@app.get("/test")
async def test():
    return {"message": f"Test endpoint"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=7000, workers=5)

