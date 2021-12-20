import logging
import hashlib
import base64
import time
import hmac
import os
import requests
import json

import azure.functions as func

def generate_token(resource_path):
    try:
        access_id = os.environ.get('LMAccessId')
        access_key = os.environ.get('LMAccessKey')
        
        AccessId = access_id
        AccessKey = access_key
        httpVerb ='GET'
        resourcePath = resource_path
        epoch = str(int(time.time() * 1000))
        requestVars = httpVerb + epoch + resourcePath
        hmac1 = hmac.new(AccessKey.encode(),msg=requestVars.encode(),digestmod=hashlib.sha256).hexdigest()
        signature = base64.b64encode(hmac1.encode())
        token = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
        logging.info(token)
        return token
    
    except:
        return "Token Invalid"


def process_lm_data(data_body,status_code):
   
    items = []
    logging.info(data_body)
    lm_hostname = os.environ.get('LM_Url')

    #### get LM dashboard id ####
    try:
        json_result = json.loads(data_body)
        dashboard_name = json_result['dashboardName']
        logging.info(dashboard_name)

        resource_path = '/dashboard/dashboards'
        dashboard_token = generate_token(resource_path)
        lm_dashboard_url = f'https://{lm_hostname}/santaba/rest/dashboard/dashboards?filter=name:{dashboard_name}'
        headers = {
        'Authorization': dashboard_token
        }

        response = requests.request("GET", url=lm_dashboard_url, headers=headers)
        data = response.json()

        dashboard_id = data["data"]["items"][0]["id"]
        logging.info(dashboard_id)
    
    
    #### get LM widget id ####
    
        resource_path = '/dashboard/dashboards/{}/widgets'.format(dashboard_id)
        widget_token = generate_token(resource_path)
        lm_widget_url = f'https://{lm_hostname}/santaba/rest/dashboard/dashboards/{dashboard_id}/widgets?filter=name:Availability Issues'
        payload={}
        headers = {
        'Authorization': widget_token
        }
        response = requests.request("GET", lm_widget_url, headers=headers)
        data = response.json()
        widget_id = data["data"]["items"][0]["id"]
    
    
    #### get LM Widget data ####
    
        resource_path = '/dashboard/widgets/{}/data'.format(widget_id)
        data_token = generate_token(resource_path)
        lm_data_url = f'https://{lm_hostname}/santaba/rest/dashboard/widgets/{widget_id}/data'
        headers = {
        'Authorization': data_token,
        'x-version': '3'
        }
        response = requests.request("GET", lm_data_url, headers=headers)
        data = response.json()
        status_code = response.status_code
        availability_data = data["resultList"]
        for row in availability_data:
            items.append({ "name" : row["bottomLabel"], "value" : row["value"] })
        lm_dashboard_result = json.dumps(items)
        logging.info(lm_dashboard_result)
        return lm_dashboard_result,status_code
    
    except:
        if response.status_code == 400:
            lm_dashboard_result = "Bad Request"
            return lm_dashboard_result,response.status_code

        elif response.status_code == 401:
            lm_dashboard_result = "Unauthorized"
            return lm_dashboard_result,response.status_code

        elif response.status_code == 500:
            lm_dashboard_result = "Internal Server Error, failed to fetch data"
            return lm_dashboard_result,response.status_code

        else:
            return lm_dashboard_result,response.status_code

# MAIN

def main(req: func.HttpRequest) -> func.HttpResponse:
    status_code = 0
    logging.info('Python HTTP trigger function processed a request.')
    
    data_body = req.get_body()
    if data_body:
        logging.info(data_body)
        get_availability_result,status_code = process_lm_data(data_body,status_code)
        return func.HttpResponse(get_availability_result,status_code)
    else:
        logging.info("Missing Data")
        return func.HttpResponse("Missing data")