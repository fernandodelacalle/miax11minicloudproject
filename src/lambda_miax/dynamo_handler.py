import pandas as pd
import boto3
from boto3.dynamodb.conditions import Key


class DynamoHandle:

    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = table_name

    def create_table(self):
        table = self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'VALOR',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'TIME',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'VALOR',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'TIME',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    def load(self, record):
        table = self.dynamodb.Table(self.table_name)
        response = table.put_item(
            Item=record
        )

    def query(self):
        table = self.dynamodb.Table(self.table_name)
        response = table.query(
            KeyConditionExpression=Key('VALOR').eq('SAN')
        )
        return response

    def upload_close_data(self, close_data, tck):
        table = self.dynamodb.Table(self.table_name)
        with table.batch_writer() as writer:
            for idx, row in close_data.items():
                price_dict = {
                    'VALOR': tck,
                    'TIME': str(idx),
                    'PRICE': str(row)
                }
                response = writer.put_item(
                    Item=price_dict
                )
