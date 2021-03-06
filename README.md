# AWS S3 Bucket Dumper

* [AWS S3 Bucket Dumper](#s3-dumper)
* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [History](#history)
* [License](#license)


## Description

Pretty simple program that downloads the entire contents of an S3 bucket to a passed directory, and displays a progress bar during the download. The AWS emulated directory structures get created like normal directories.

![demo](https://github.com/shellraiser/aws-s3-bucket-dumper/blob/main/docs/demo.gif)

### Usage

#### From terminal

Clone and install requirements first.

```
git clone https://github.com/shellraiser/aws_s3_dumper.git
cd aws_s3_dumper
pip3 install -r requirements.txt --upgrade
python3 aws_s3_dumper.py
```

There is a config.ini where you can pass the parameters for the script:

```
s3_access_key =
s3_secret_key =
aws_session_token =
aws_region =
download_directory =
```

If you do not fill out the config.ini, you'll be prompted to enter the following. I use gimme-aws-creds to get my keys (https://github.com/Nike-Inc/gimme-aws-creds).

The region should be the full bucket region name (ie us-east-1, ap-southeast-1, etc.)

```
Enter in the AWS Access Key:
Enter in the AWS Secret Key:
Enter in the S3 Bucket name:
Enter in the AWS region:
Please specify a directory where you \
would like to put the downloaded S3 bucket (a new folder will \
be created under this directory with the S3 bucket name):
```

After the initial AWS connection, you'll be asked if you want to do a check for disk space. This will first check the full size of all objects added up in the bucket, then compare it to the available disk space on the drive your directory is in. 

Upon downloading, a bar will be displayed to show total objects and progress.

## History
   * 0.1.1 - Adding a progress bar for downloads
   * 0.1.0 - Initial commit

## License

Open Source, use as you will! 

