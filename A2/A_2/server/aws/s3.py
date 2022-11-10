import boto3
from botocore.exceptions import ClientError

class Bucket:
    def __init__(self, bucket_name) -> None:
        self.client = boto3.client("s3")
        self.bucket_name = bucket_name
        self.object = self.Object(self.client, self.bucket_name)
        self.create()

    def list(self):
        resp = self.client.list_buckets()
        if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True, [i["Name"] for i in resp["Buckets"]]
        return False, resp

    def create(self):
        resp = self.client.create_bucket(Bucket=self.bucket_name)
        if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True, resp
        return False, resp

    def delete(self):
        resp = self.client.delete_bucket(Bucket=self.bucket_name)
        if resp["ResponseMetadata"]["HTTPStatusCode"] == 204:
            return True, resp
        return False, resp

    class Object:
        def __init__(self, client, bucket_name) -> None:
            self.client = client
            self.bucket = bucket_name

        def upload(self, binary_data, key):
            resp = self.client.put_object(Body=binary_data, Bucket=self.bucket, Key=key)
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True, resp
            return False, resp
        
        def get(self, key):
            try:
                resp = self.client.get_object(Bucket=self.bucket, Key=key)
                if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    return True, resp["Body"].read().decode("utf-8")
                return False, resp
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchKey':
                    return False, {"error": "No such key"}
                else:
                    raise
        
        def list(self):
            resp = self.client.list_objects_v2(Bucket=self.bucket)
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True, [i["Key"] for i in resp["Contents"]] if resp["KeyCount"] > 0 else []
            return False, resp

        def delete(self, key):
            resp = self.client.delete_object(Bucket=self.bucket, Key=key)
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 204:
                return True, resp
            return False, resp