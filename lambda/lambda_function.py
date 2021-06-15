from botocore.exceptions import ClientError
from cryptography.fernet import Fernet
import base64
import boto3
import json
import os

# https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-lib
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret():
    aws_secret_name = os.environ['SECRET_ARN']
    aws_region_name = os.environ['SECRET_REGION']

    boto3_session = boto3.session.Session()
    secretsmanager = boto3_session.client(
        service_name='secretsmanager',
        region_name=aws_region_name
    )

    try:
        get_secret_value_response = secretsmanager.get_secret_value(
            SecretId=aws_secret_name
        )
    except ClientError as e:
        print("Unexpected error: %s" % e)
        raise
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    return secret


def lambda_handler(event, context):
    aws_secret_value = json.loads(get_secret())
    key_string = aws_secret_value['ENCRYPTION_KEY']
    key = key_string.encode('utf-8')
    f = Fernet(key)

    logger.info("Request event:")
    # Specifying separators removes all prettifying and prints a single line:
    # Improves formatting in CWLogs web consule and ensures plain JSON
    logger.info(json.dumps(event, separators=(',', ':')))

    response_body = {}

    if event['headers'].get('cookie', '') != '':
        response_body['headers'] = {
            'cookie': event['headers']['cookie']
        }

    # Escape JSON, convert to UTF-8 byte string, and encrypt
    body_bytes = json.dumps(response_body, separators=(',', ':')).encode('utf-8')
    body_encrypted = f.encrypt(body_bytes).decode('utf-8')

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain"
        },
        "body": body_encrypted
    }

    logger.info("Response:")
    logger.info(json.dumps(response, separators=(',', ':')))

    return response
