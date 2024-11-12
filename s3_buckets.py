#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError
import logging


def create_bucket(endpoint_url, access_key, secret_key, bucket_name, region=None):
    """
    Create a bucket on Ceph Object Storage using the S3 API and boto3.

    Parameters:
        endpoint_url (str): The endpoint URL for the Ceph Object Gateway.
        access_key (str): The access key for authentication.
        secret_key (str): The secret key for authentication.
        bucket_name (str): The name of the bucket to create.
        region (str, optional): The region where the bucket will be created (default: None).

    Returns:
        bool: True if the bucket was created successfully, False otherwise.
    """
    try:
        # Create a boto3 S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url="https://%s" % endpoint_url,
        )

        # Create the bucket
        if region:
            # If a region is specified
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        else:
            # Default region
            s3_client.create_bucket(Bucket=bucket_name)

        logging.info(f"Bucket '{bucket_name}' created successfully.")
        return True

    except ClientError as e:
        logging.error(f"An error occurred while creating the bucket: {e}")
        return False


def get_bucket_policy(endpoint_url, access_key, secret_key, bucket_name):
    """
    Retrieve the S3 bucket policy of a specific bucket on Ceph Object Storage using boto3.

    Parameters:
        endpoint_url (str): The endpoint URL for the Ceph Object Gateway.
        access_key (str): The access key for authentication.
        secret_key (str): The secret key for authentication.
        bucket_name (str): The name of the bucket.

    Returns:
        str: The bucket policy as a JSON string, or None if no policy is found.
    """
    try:
        # Create a boto3 S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url="https://%s" % endpoint_url,
        )

        # Retrieve the bucket policy
        response = s3_client.get_bucket_policy(Bucket=bucket_name)
        policy = response["Policy"]
        return policy

    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
            logging.warning(f"No policy found for bucket '{bucket_name}'.")
            return None
        else:
            logging.error(f"An error occurred: {e}")
            return None


def set_bucket_policy(endpoint_url, access_key, secret_key, bucket_name, policy):
    """
    Set the S3 bucket policy for a specific bucket on Ceph Object Storage using boto3.

    Parameters:
        endpoint_url (str): The endpoint URL for the Ceph Object Gateway.
        access_key (str): The access key for authentication.
        secret_key (str): The secret key for authentication.
        bucket_name (str): The name of the bucket.
        policy (dict): The bucket policy as a dictionary.

    Returns:
        bool: True if the policy was set successfully, False otherwise.
    """
    try:
        # Create a boto3 S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url="https://%s" % endpoint_url,
        )

        # Set the bucket policy
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=policy)
        return True

    except ClientError as e:
        logging.error(f"An error occurred: {e}")
        return False
