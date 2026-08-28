import os

from dotenv import load_dotenv
load_dotenv()

aws_bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadMKImages",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{os.getenv('S3_BUCKET_NAME')}/*"
        }
    ]
}

aws_iam_policy = {
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": ["s3:PutObject"],
			"Resource": f"arn:aws:s3:::{os.getenv('S3_BUCKET_NAME')}/*"
		}
	]
}