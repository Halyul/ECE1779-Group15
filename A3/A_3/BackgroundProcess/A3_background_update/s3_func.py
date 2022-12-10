import boto3

import config

s3 = boto3.client("s3")
bucket_name = config.bucket_name

def get_image_from_s3(image_name):
    response = s3.get_object(Bucket=bucket_name, Key=image_name)
    file_data = response["Body"].read()
    return file_data

def save_image_to_s3(byte_data, new_image_name):
    s3.put_object(Body = byte_data, Bucket=bucket_name, Key=new_image_name)
    return