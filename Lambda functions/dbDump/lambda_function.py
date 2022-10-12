import json
import urllib3
import boto3
from decimal import Decimal
import time
from botocore.exceptions import ClientError

api_key = 'thyLn1T11o_zBPVAYc-WVbuBMyWuZs15berl26CLRpWwHhMqAMJzcULWSQOKFIWgawkrNpHrgRDWP-W0HVKTMMBQuB7O5JZAc7jFcu8_k2WgFlrCCsmVkl5Uso46Y3Yx'
headers = {'Authorization': 'Bearer %s' % api_key}
url = "https://api.yelp.com/v3/businesses/search"

def lambda_handler(event, context):
    TODO implement
    http = urllib3.PoolManager()
    foodTypes = ["French","Chinese", "Japanese", "Indian", "Italian", "Greek", "Spanish", "Lebanese", "Moroccan", "Turkish", "Thai"]
    for k in range(11):
        for i in range(20):
            params = {'term': foodTypes[k], 'location': 'Manhattan','limit':50,'offset':i*50}
            r = http.request(
            'GET',
            url,
            headers=headers,
            fields=params)
            res = json.loads(r.data, parse_float=Decimal)
            dinning = []
            length = len(res["businesses"])
            for j in range(length):
                id = res["businesses"][j]["id"]
                name = res["businesses"][j]["name"]
                address = res["businesses"][j]["location"]["address1"]
                coordinates = str(res["businesses"][j]["coordinates"]["latitude"]) + ", " + str(res["businesses"][j]["coordinates"]["longitude"])
                zip = res["businesses"][j]["location"]["zip_code"]
                rating = res["businesses"][j]["rating"]
                review_count = res["businesses"][j]["review_count"]
                dinning.append({
                    "id": id,
                    "name": name,
                    "address" : address,
                    "coordinates": coordinates,
                    "zip": zip,
                    "rating": rating,
                    "review_count" : review_count,
                    "cuisine": foodTypes[k]
                })
            insert_data(dinning)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def insert_data(data_list, db=None, table='yelp-restaurants'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    # overwrite if the same index is provided
    for data in data_list:
        table.put_item(Item=data)
    return