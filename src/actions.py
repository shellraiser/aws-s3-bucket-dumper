import boto3
import os
import shutil
import sys

def downloadbucketobjects(botosession,s3_bucket,download_directory):
    """Get the list of objects in the bucket, using pagination
    """

    print("Creating folder for bucket objects...")

    downloadpath = os.path.join(download_directory, s3_bucket)

    if os.path.exists(downloadpath):
        usercontinue = ''
        while usercontinue != 'y' or 'n':
            usercontinue = input("Folder already exists. Do you want to overwrite it? y/n ")
            if usercontinue == 'n':
                sys.exit(1)
            elif usercontinue == 'y':
                shutil.rmtree(downloadpath)
                break
            else:
                print("Wrong input entered. Please enter either y or n")

    os.mkdir(downloadpath)

    print("Created " + downloadpath)

    s3resource = botosession.resource('s3')
    bucket = s3resource.Bucket(s3_bucket)
    objects = bucket.objects.all()

    s3client= botosession.client('s3')

    print("Downloading objects from bucket...")

    for object in objects:
        s3_key = object.key

        path, filename = os.path.split(s3_key)
        objectpath = "/".join((downloadpath,path))
        if len(path) != 0 and not os.path.exists(objectpath):
            os.makedirs(objectpath)
        if not s3_key.endswith("/"):
            download_to = objectpath + '/' + filename if objectpath else filename
            s3client.download_file(s3_bucket, s3_key, download_to)

    print("All objects have been downloaded.")