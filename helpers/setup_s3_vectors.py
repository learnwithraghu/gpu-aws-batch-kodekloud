#!/usr/bin/env python3
"""Create the S3 Vector bucket and CLIP caption index used by the course."""

import argparse
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from s3_vectors import CLIP_DIMENSION


def main():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    parser = argparse.ArgumentParser(description="Create the course S3 Vector bucket and index.")
    parser.add_argument("--region", default=os.environ.get("AWS_DEFAULT_REGION", "ap-northeast-1"))
    parser.add_argument("--vector-bucket", default=os.environ.get("S3_VECTOR_BUCKET"))
    parser.add_argument("--index", default=os.environ.get("S3_VECTOR_INDEX", "image-captions"))
    parser.add_argument("--dry-run", action="store_true", help="Print the resources without creating them")
    args = parser.parse_args()

    account_id = boto3.client("sts", region_name=args.region).get_caller_identity()["Account"]
    vector_bucket = args.vector_bucket or f"gpu-teaching-vectors-{account_id}"
    print(f"Region        : {args.region}")
    print(f"Vector bucket : {vector_bucket}")
    print(f"Vector index  : {args.index}")
    print(f"Configuration : float32, {CLIP_DIMENSION} dimensions, cosine distance")
    if args.dry_run:
        return

    client = boto3.client("s3vectors", region_name=args.region)
    try:
        client.get_vector_bucket(vectorBucketName=vector_bucket)
        print("Vector bucket already exists.")
    except ClientError as error:
        if error.response["Error"]["Code"] not in {"NotFoundException", "ResourceNotFoundException"}:
            raise
        client.create_vector_bucket(vectorBucketName=vector_bucket)
        print("Created vector bucket.")

    try:
        client.get_index(vectorBucketName=vector_bucket, indexName=args.index)
        print("Vector index already exists.")
    except ClientError as error:
        if error.response["Error"]["Code"] not in {"NotFoundException", "ResourceNotFoundException"}:
            raise
        client.create_index(
            vectorBucketName=vector_bucket,
            indexName=args.index,
            dataType="float32",
            dimension=CLIP_DIMENSION,
            distanceMetric="cosine",
        )
        print("Created vector index.")


if __name__ == "__main__":
    main()