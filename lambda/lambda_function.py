from botocore.exceptions import ClientError
from cryptography.fernet import Fernet
import base64
import boto3
import json
import os

# Use the recommended logger in Lambda
# https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-lib
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_secret():
    # Simplify and adapt the code sample from AWS Secrets Manager

    # Secret ARN provided by the environment
    aws_secret_name = os.environ['SECRET_ARN']
    logger.info(f"aws_secret_name={aws_secret_name}")

    # Secret region can be provided by the environment or determined by the full ARN
    if os.environ.get('SECRET_REGION', '') != '':
        aws_region_name = os.environ['SECRET_REGION']
    else:
        aws_region_name = aws_secret_name.split(':')[3]
    logger.info(f"aws_region_name={aws_region_name}")

    # boto3 session needs to be in the same region as the secret
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
    # Log the incoming request for debugging
    logger.info("Request event:")
    # Specifying separators removes all prettifying and prints a single line;
    # Improves formatting in CWLogs web console and ensures plain JSON
    logger.info(json.dumps(event, separators=(',', ':')))

    # Default response is "Bad Request" and an empty response body
    response_code = 400
    response_body = ""

    # If 'cookie' is under 'headers', set the value as the encrypted response body
    if event['headers'].get('cookie', '') != '':
        # OK
        response_code = 200

        # Read the encryption secret from AWS Secrets Manager as a Fernet key
        aws_secret_value = json.loads(get_secret())
        key_string = aws_secret_value['ENCRYPTION_KEY']
        key = key_string.encode('utf-8')
        f = Fernet(key)

        # Convert to UTF-8 byte string for Fernet, and encrypt
        cookie_encoded = str(event['headers']['cookie']).encode('utf-8')
        response_body = f.encrypt(cookie_encoded).decode('utf-8')

    # Send back the format required for ALB
    response = {
        "statusCode": response_code,
        "headers": {
            "Content-Type": "text/plain"
        },
        "body": response_body
    }

    logger.info("Response:")
    logger.info(json.dumps(response, separators=(',', ':')))

    return response