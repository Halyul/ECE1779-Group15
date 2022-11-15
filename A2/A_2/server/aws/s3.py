import boto3
from botocore.exceptions import ClientError
import logging

class Bucket:
    def __init__(self, bucket_name) -> None:
        self.client = boto3.client("s3")
        self.bucket_name = bucket_name
        self.object = self.Object(self.client, self.bucket_name)
    #     self.create()

    # def list(self):
    #     resp = self.client.list_buckets()
    #     if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
    #         logging.info("List buckets: {}".format(resp))
    #         return True, [i["Name"] for i in resp["Buckets"]]
    #     logging.error("List buckets: {}".format(resp))
    #     return False, resp

    # def create(self):
    #     resp = self.client.create_bucket(Bucket=self.bucket_name)
    #     if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
    #         logging.info("Create bucket: {}".format(resp))
    #         return True, resp
    #     logging.error("Create bucket: {}".format(resp))
    #     return False, resp

    # def delete(self):
    #     resp = self.client.delete_bucket(Bucket=self.bucket_name)
    #     if resp["ResponseMetadata"]["HTTPStatusCode"] == 204:
    #         logging.info("Delete bucket: {}".format(resp))
    #         return True, resp
    #     logging.error("Delete bucket: {}".format(resp))
    #     return False, resp

    class Object:
        def __init__(self, client, bucket_name) -> None:
            self.client = client
            self.bucket = bucket_name

        def upload(self, binary_data, key):
            resp = self.client.put_object(Body=binary_data, Bucket=self.bucket, Key=key)
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logging.info("Upload S3 object")
                return True, resp
            logging.error("Upload S3 object: {}".format(resp))
            return False, resp
        
        def get(self, key):
            try:
                resp = self.client.get_object(Bucket=self.bucket, Key=key)
                if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    logging.info("Get S3 object")
                    return True, resp["Body"].read().decode("utf-8")
                logging.error("Get S3 object: {}".format(resp))
                return False, resp
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchKey':
                    logging.error("Get S3 object: {}".format(e))
                    return False, {"error": "No such key"}
                else:
                    raise
        
        def list(self):
            resp = self.client.list_objects_v2(Bucket=self.bucket)
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logging.info("List S3 objects")
                return True, [i["Key"] for i in resp["Contents"]] if resp["KeyCount"] > 0 else []
            logging.error("List objects: {}".format(resp))
            return False, resp

        def delete(self, key):
            resp = self.client.delete_object(Bucket=self.bucket, Key=key)
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 204:
                logging.info("Delete S3 object")
                return True, resp
            logging.error("Delete S3 object: {}".format(resp))
            return False, resp
        
        def delete_all(self):
            resp = self.client.delete_objects(Bucket=self.bucket, Delete={"Objects": [{"Key": i} for i in self.list()[1]]})
            if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
                logging.info("Delete S3 objects")
                return True, resp
            logging.error("Delete S3 objects: {}".format(resp))
            return False, resp