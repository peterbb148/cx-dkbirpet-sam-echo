import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def get_item(event):

    #dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('dkbirpet')      

    try:
        response = table.query(
            KeyConditionExpression=Key('id').eq(event['pathParameters']['id'])
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']

def get_items(event):

    #client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
    client = boto3.client('dynamodb')
    table_name = 'dkbirpet'

    results = []
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = client.scan(
                TableName=table_name,
                ExclusiveStartKey=last_evaluated_key
            )
        else: 
            response = client.scan(TableName=table_name)
        last_evaluated_key = response.get('LastEvaluatedKey')
        
        results.extend(response['Items'])
        
        if not last_evaluated_key:
            break
    return results

def create_item(event, dynamodb=None):

    if not dynamodb:
        #dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('dkbirpet')

    # try:

    id = uuid.uuid4().hex
    response = table.put_item(
    Item={
            'id': id,
            'message': event['body']['message']
            }
    )
    # except ClientError as e:
    #     print(e.response['Error']['Message'])
    return id

def delete_item(event):

        #dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb')
        
        table = dynamodb.Table('dkbirpet')
        item = get_item(id)
        response = table.delete_item(
            Key={
                'id': event['body']['id'],
                'message': event['body']['message']
            }
        )
        return response

# map the inputs to the functions
options = {'GET' : get_item,
           'GETS' : get_items,
           'POST' : create_item,
           'DELETE' : delete_item,
}

def handler(event, context):

    method = event['httpMethod']
    if method == "GET" and event['path'] == "/echo":
        method = 'GETS'
    elif method == "GET" and event['pathParameters']['id'] != "":
        method = 'GET'
    if method == 'POST':
        print(event)

    print("Method:" + method)
    body = {
        "result": options[method](event)
    }
    response = {
        "statusCode": 200,
        'body': json.dumps(body)
    }

    return response
