import boto3
import json
import os
from datetime import datetime
from botocore.exceptions import ClientError

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "minioadmin"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
        )
        self.bucket_name = "avd-raw-data"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
            except Exception as e:
                print(f"Error creating bucket: {e}")

    def save_json(self, data: dict, filename: str = None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"thermal_data_{timestamp}.json"
        
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=json.dumps(data, default=str)
            )
            return f"s3://{self.bucket_name}/{filename}"
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return None
