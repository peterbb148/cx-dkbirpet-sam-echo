# SAM

## Create virtual Python environment

```
pipenv --python /usr/local/opt/python@3.9/bin/python3
```

and to start environment run:

```
pipenv shell
```

## To build locally

```
sam build
```

## To start locally

```
sam local start-api -t template.yaml
```

## Deploy

```
sam deploy --guided
```

## Run DynamoDB locally

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.UsageNotes.html

```
docker pull amazon/dynamodb-local
docker run -p 8000:8000 amazon/dynamodb-local
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

Create table in DynamoDB
```
aws dynamodb create-table --table-name dkbirpet --attribute-definitions AttributeName=id,AttributeType=S AttributeName=message,AttributeType=S --key-schema AttributeName=id,KeyType=HASH AttributeName=message,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --endpoint-url http://localhost:8000
```

Verify table creation
```
 aws dynamodb describe-table --table-name dkbirpet --endpoint-url http://localhost:8000
```

Create an item
```
aws dynamodb put-item --table-name dkbirpet --item '{"id": {"S": "abc"}, "message": {"S": "Call Me Today"}}' --return-consumed-capacity TOTAL --endpoint-url http://localhost:8000
```

Use scan to return all items
```
aws dynamodb scan --table-name dkbirpet --endpoint-url http://localhost:8000
```
Use query to find a specific item (yes, still need to figure this out on the command line :anguished:)
```
aws dynamodb query --table-name dkbirpet  --endpoint-url http://localhost:8000
```