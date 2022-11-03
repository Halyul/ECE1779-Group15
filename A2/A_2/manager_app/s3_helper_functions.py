import boto3


def s3_list():
    s3 = boto3.resource('s3')
    buckets = s3.buckets.all()
    return buckets


def s3_clear(bucket_name):
    s3 = boto3.client('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.delete()
    # Use the following code for versioned bucket
    # bucket.object_versions.delete()
