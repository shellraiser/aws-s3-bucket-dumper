import boto3
import sys

def connect_botosession(s3_access_key,s3_secret_key,aws_session_token,aws_region):

    try:
    
        botosession = boto3.Session(
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key,
            aws_session_token=aws_session_token,
            region_name=aws_region)

        return botosession

    except Exception as error:
        print(error)
        sys.exit(1)