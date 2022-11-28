import json
import os
import logging
from urllib import response
from urllib.parse import urljoin
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SNIPE_URL = os.environ['SNIPE_URL']
SNIPE_TOKEN = os.environ['SNIPE_TOKEN']

headers = {
    "accept" : "application/json",
    "content-type": "application/json",
    "Authorization" : "Bearer " + SNIPE_TOKEN
}

    
def search_model(modelName,SERIAL):
    models_url = urljoin(SNIPE_URL , "/api/v1/models?limit=50&offset=0&search=")
    models_url = models_url + modelName

    response = requests.get(models_url,headers=headers)
    json_data = json.loads(response.text)

    if json_data['total'] > 0 :
        #モデルIDを取得する
        model_id = json_data['rows'][0]['id']
    else:
        #モデルを作成する
        create_model_ret = create_model(modelName)
        print(create_model_ret)
        if create_model_ret['status'] != 'success':
            logger.error('モデル作成エラー')
        else:
            model_id = create_model_ret['payload']['id']

    ret = create_asset(model_id,SERIAL)
    print(ret)


def create_model(modelName):
    url = urljoin(SNIPE_URL, "/api/v1/models")
    #拡張フィールドセットIDにJamf用をセットして作成する
    payload = {
        "name" : modelName,
        "model_number" : modelName,
        "category_id" : 2,
        "manufacturer_id" : 1,
        "fieldset_id" : 2 
    }
    response = requests.post(url,headers=headers,json=payload)
    ret = json.loads(response.text)
    return ret

def create_asset(model_id,serialNo):
    url = urljoin(SNIPE_URL, "/api/v1/hardware")
    payload = {
        "name"      : serialNo,
        "serial"    : serialNo,
        "asset_tag" : serialNo,
        "status_id" : 5,
        "model_id"  : model_id,
        "archived"  : "false"
    }
    response = requests.post(url,headers=headers,json=payload)
    ret = json.loads(response.text)
    return ret

def lambda_handler(event, context):
    body = json.loads(event['body'])
    # 必要データを取得する
    SERIAL = body['event']['serialNumber']
    MODEL = body['event']['model']
    search_model(MODEL,SERIAL)
    
    return {
        'statusCode': 200,
        'body': 'OK'
    }