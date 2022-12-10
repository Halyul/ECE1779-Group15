import requests
import boto3

import config

api_key = config.api_key
api_secret = config.api_secret

bucket_name = config.bucket_name

def file_upload(file_data):
    # send this image to the upload image API and get an upload_id
    response = requests.post(
        'https://api.imagga.com/v2/uploads',
        auth=(api_key, api_secret),
        files={'image': file_data})
    try:
        response = response.json()
        # print(response)
        if response['status']['type'] == 'success':
            return response['result']['upload_id']
        else:
            return 'failed'
    except Exception as e:
        print("{}".format(e))
        return 'failed'
    
def tagging(upload_id):
    # use the upload id to get the tag of this image
    response = requests.get(
        'https://api.imagga.com/v2/tags?image_upload_id=' + upload_id,
        auth=(api_key, api_secret))
    try:
        response = response.json()
        # print(response)
        if response['status']['type'] == 'success':
            return response['result']['tags'][0]['tag']['en']
    except:
        return "failed"

def do_tag(file_data):
    upload_id = file_upload(file_data)
    if upload_id != 'failed':
        tag = tagging(upload_id)
        return tag
    else:
        return 'failed'