import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    email = event["interpretations"][0]['intent']['slots']['phone']['value']['originalValue']
    cuisine = event["interpretations"][0]['intent']['slots']['cuisine']['value']['originalValue']
    
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/210882669999/DiningMQ'
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'The Whistler'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'None'
            },
            'WeeksOn': {
                'DataType': 'Number',
                'StringValue': '6'
            }
        },
        MessageBody=(
            email + "," + cuisine
        )
    )
    print(response['MessageId'])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
