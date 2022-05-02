import os
import sys
import requests
import random
from fastapi import FastAPI, Response
sys.path.append(os.path.dirname(os.getcwd()))
# from deployment.main import BASE_RECOMMENDATIONS
import subprocess
import time

BASE_RECOMMENDATIONS = ['the+wrong+trousers+1993', 'a+close+shave+1995', 'viy+1967', 'alaskaland+2013', 'one+flew+over+the+cuckoos+nest+1975', 
                'casablanca+1942', 'lawrence+of+arabia+1962', 'cool+hand+luke+1967', 'crouching+tiger_+hidden+dragon+2000', 
                'shrek+2001', 'lethal+weapon+2+1989', 'the+untouchables+1987', 'one+flew+over+the+cuckoos+nest+1975', 
                'the+dark+knight+2008', 'the+bridge+on+the+river+kwai+1957', 'vertigo+1958', 'american+beauty+1999', 'fargo+1996', 
                'rear+window+1954', 'citizen+kane+1941']

app = FastAPI()

global ports
ports = [7004, 7005, 7006, 7007, 7008]


def get_port():
    global ports
    # print(f"available ports: {ports}")
    try:
        return random.choice(ports)
    except:
        return None

@app.get("/recommend/{user_id}")
async def recommend(user_id: int):

    selected_port = get_port()
    if selected_port is None:
        return Response(','.join(BASE_RECOMMENDATIONS))
    
    url = f'http://17645-team12.isri.cmu.edu:{selected_port}/recommend/'
    refresh_url = f'http://17645-team12.isri.cmu.edu:7000/refresh_ports/'+str(selected_port)

    try:
        response = requests.get(url+str(user_id)).text
        return Response(response)
    except:
        ports.remove(selected_port)
        print("-------------------------------------------------------------------------")
        requests.get(refresh_url, timeout=0.00000000001)
        return Response(','.join(BASE_RECOMMENDATIONS))


@app.get('/add_port/{port}')
async def add_port(port: int):
    global ports
    ports.append(port)
    return Response(f"added port: {port}")

@app.get('/remove_port/{port}')
async def remove_port(port: int):
    global ports
    ports.remove(port)
    return Response(f"removed port: {port}")

@app.get('/refresh_port/')
async def refresh_ports(port: int):
    time.sleep(5)
    global ports
    ports.append(port)
    print(f"Refreshed port: {ports}")
    print("***************************************************************************")
    return Response(f"refreshed ports: {ports}")
