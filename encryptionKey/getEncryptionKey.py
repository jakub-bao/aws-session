#!/usr/bin/python3
import base64
import boto3
import os

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
    except:
        print("Unexpected error:")
        raise
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    return secret

print(get_secret())