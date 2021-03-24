import boto3
import botocore
import sys
from datetime import datetime, timedelta
import shutil

def varcheck(s3_access_key,s3_secret_key,aws_session_token,s3_bucket,aws_region,download_directory):
    """Check to make sure all required variables are passed. If not,
    prompt for them. """

    if s3_access_key is 'None':
        s3_access_key = input("Enter in the AWS Access Key ID: ")
    if s3_secret_key is 'None':
        s3_secret_key = input("Enter in the AWS Secret Key: ")
    if aws_session_token is 'None':
        aws_session_token = input("Enter in the AWS Session Token: ")
    if s3_bucket is 'None':
        s3_bucket = input("Enter in the S3 Bucket name: ")
    if aws_region is 'None':    
        aws_region = input("Enter in the AWS region: ")
    if download_directory is 'None':    
        download_directory = input("Please specify a directory where you \
would like to put the downloaded S3 bucket (a new folder will \
be created under this directory with the S3 bucket name): ")


def bucketsize(botosession,s3_bucket):
    """Get the size of the bucket and print out to display
    to user """
    
    print("Getting S3 bucket total size...")

    cloudwatch = botosession.client('cloudwatch')

    try:

        sizeresponse = cloudwatch.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'string',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/S3',
                            'MetricName': 'BucketSizeBytes',
                            'Dimensions': [
                                {
                                    'Name': 'BucketName',
                                    'Value': s3_bucket
                                },
                                {
                                    'Name': 'StorageType',
                                    'Value': 'StandardStorage'
                                }
                            ]
                        },
                        'Stat': 'Average',
                        'Period': 3600,
                        'Unit': 'Bytes'
                    },
                    'ReturnData': True,
                },
            ],
            StartTime=datetime.now() - timedelta(days=1),
            EndTime=datetime.now()
        )

        total_bytes = sum(sizeresponse['MetricDataResults'][0]['Values'])
        total_gigs = round((total_bytes/1024/1024/1024),4)
        
        countresponse = cloudwatch.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'string',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/S3',
                            'MetricName': 'NumberOfObjects',
                            'Dimensions': [
                                {
                                    'Name': 'BucketName',
                                    'Value': s3_bucket
                                },
                                {
                                    'Name': 'StorageType',
                                    'Value': 'AllStorageTypes'
                                }
                            ]
                        },
                        'Stat': 'Average',
                        'Period': 3600,
                        'Unit': 'Count'
                    },
                    'ReturnData': True,
                },
            ],
            StartTime=datetime.now() - timedelta(days=1),
            EndTime=datetime.now()
        )

        objectnum = sum((countresponse['MetricDataResults'][0]['Values']))
        
        print("Total number of objects: " + str(int((objectnum))))
        print("Total size of bucket in Bytes: " + str(int(total_bytes)) + "KB")
        print("Total size of bucket in Gigabytes: " + str(int(total_gigs)) + "GB")

        return total_bytes

    except Exception as error:
        print(error)
        sys.exit(1)

def checkfreespace(download_directory,total_bytes):
    """ Check free space of computer and compare it to total
    bucket size """

    print("Checking available disk space...")

    diskusage = shutil.disk_usage(download_directory)
    freediskspace_bytes = diskusage[2]
    freediskspace_gigs = round((freediskspace_bytes/1024/1024/1024),4)

    print("Available disk space in Bytes: " + str(int(freediskspace_bytes)) + "KB")
    print("Available disk space in Gigabytes: " + str(int(freediskspace_gigs )) + "GB")

    if freediskspace_bytes < total_bytes:
        print("Not enough disk space to download this bucket. \
            Please start over and select a new disk location.")
        exit

    usercontinue = ''

    while usercontinue != 'y' or 'n':
        print("Looks good! Current available disk space is more than bucket size.")
        usercontinue = input("Do you want to continue? y/n ")

        if usercontinue == 'n':
            sys.exit(1)
        elif usercontinue == 'y':
            break
        else:
            print("Wrong input entered. Please enter either y or n")