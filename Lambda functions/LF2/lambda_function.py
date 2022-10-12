import json
import boto3
from botocore.exceptions import ClientError
import requests
from requests_aws4auth import AWS4Auth
import random

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-restaurants-zbf6leytbwshcqce36fulwguqm.us-east-1.es.amazonaws.com'
index = 'restaurants'
url = host + '/' + index + '/_search'


def lambda_handler(event, context):
    
    receive = event['Records'][0]['body']
    re_temp = receive.split(",")
    cuisine = re_temp[1]
    email = re_temp[0]
    
    query = {
        "size": 100,
        "query": {
            "match": {
                "cuisine": cuisine
            }
        }
    }

    headers = {"Content-Type": "application/json"}
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    res = json.loads(r.text)
    length = len(res['hits']['hits'])
    rd = random.randint(0,length - 1)
    rest_id = res['hits']['hits'][rd]['_source']['id']
    rest_info = lookup_data({'id': rest_id})
    
    message = "id: " + rest_info["id"] + "\n" + "name: " + rest_info["name"] + "\n" + "address: " + rest_info["address"] + "\n" + "coordinates: " + rest_info["coordinates"] + "\n" + "num_of_reviews: " + str(rest_info["review_count"]) + "\n"+ "rating: " + str(rest_info["rating"]) + "\n"+ "zip_code: " + str(rest_info["zip"]) + "\n"
    print(email, cuisine, message)
    
    client = boto3.client('sns')
    snsArn = 'arn:aws:sns:Region:AccountID:TestTopic'
    
    client.publish(
        TopicArn = "arn:aws:sns:us-east-1:210882669999:DiningSNS",
        Message = message ,
        Subject='Suggestion of Restaurants'
    )
    response = {
        "statusCode": 200,
        # "body": message
    }
    
    return response

def lookup_data(key, db=None, table='yelp-restaurants'):
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
        return response['Item']