#!/usr/bin/env python3
from configparser import ConfigParser

from src.connect import connect_botosession
from src.precheck import bucketsize,checkfreespace,varcheck
from src.actions import downloadbucketobjects

parser = ConfigParser() 

def main():
    print("AWS S3 BUCKET DUMPER")
    print("--------------------")
    print("This script will download the entire contents of \
an S3 bucket into a local directory. An optional pre-check for disk space is available.")
    print("--------------------")

    parser.add_section('default')
    parser.set('default', 's3_access_key', 'None')
    parser.set('default', 's3_secret_key', 'None')
    parser.set('default', 'aws_session_token', 'None')
    parser.set('default', 's3_bucket', 'None')
    parser.set('default', 'aws_region', 'None')
    parser.set('default', 'download_directory', 'None')

    parser.read('config.ini')
    s3_access_key = parser.get('default', 's3_access_key')
    s3_secret_key = parser.get('default', 's3_secret_key')
    aws_session_token = parser.get('default', 'aws_session_token')
    s3_bucket = parser.get('default', 's3_bucket')
    aws_region = parser.get('default', 'aws_region')
    download_directory = parser.get('default', 'download_directory')

    varcheck(s3_access_key,s3_secret_key,aws_session_token,s3_bucket,aws_region,download_directory)

    print("--------------------")

    print("Connecting to AWS...")

    botosession = connect_botosession(s3_access_key, s3_secret_key, aws_session_token, aws_region)

    precheck_input = ''

    while precheck_input != 'y' or 'n':

        precheck_input = input("Perform pre-checks for diskspace (recommended)? y/n: ")
        
        if precheck_input == 'n':
            break

        elif precheck_input == 'y':

            total_bytes = bucketsize(botosession,s3_bucket)
            checkfreespace(download_directory,total_bytes)
            break

        else:
            print("Wrong input entered. Please enter either y or n")

    downloadbucketobjects(botosession,s3_bucket,download_directory)

if __name__ == "__main__":
   main()
