import os
import boto3

import logging
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()

class _S3:
    def __init__(self):
        self._region_name = os.getenv('S3_REGION_NAME')
        self._aws_access_key_id = os.getenv('S3_ACCESS_KEY_ID')
        self._aws_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
        self._bucket_name = os.getenv('S3_BUCKET_NAME')
        self._client = boto3.client("s3", 
                            region_name=self._region_name,
                            aws_access_key_id=self._aws_access_key_id,
                            aws_secret_access_key=self._aws_secret_access_key
                        )
    
    def upload_image(self, image, s3_key):
        logger.info(f"Preparing to upload image to S3: bucket={self._bucket_name}, s3_key={s3_key}.")
        try:
            self._client.put_object(
                Bucket=self._bucket_name,
                Key=s3_key,
                Body=image["image_bytes"],
                ContentType=f"{image['maintype']}/{image['subtype']}"
            )
            logger.info(f"Successfully uploaded image to S3: bucket={self._bucket_name}, s3_key={s3_key}.")
        except Exception as e:
            logger.error(f"Failed to upload image: {str(e)}")
            
    def get_image_url(self, s3_key):
        return f"https://{self._bucket_name}.s3.{self._region_name}.amazonaws.com/{s3_key}"
        
s3 = _S3()