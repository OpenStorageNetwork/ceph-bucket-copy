from rgwadmin import RGWAdmin
from urllib.parse import quote
import logging


def list_all_users(host, admin_access_key, admin_secret_key, secure=True):
    """
    List all users in an RGW cluster using the rgwadmin package.

    Parameters:
        host (str): The RGW admin host URL.
        access_key (str): The access key for authentication.
        secret_key (str): The secret key for authentication.
        secure (bool): Use HTTPS if True, otherwise HTTP.

    Returns:
        list: A list of usernames.
    """
    try:
        # Initialize the RGWAdmin client
        rgw = RGWAdmin(
            access_key=admin_access_key,
            secret_key=admin_secret_key,
            server=host,
            secure=secure,
        )

        # Fetch the list of users
        users = rgw.get_users()
        return users

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []


def get_user(host, admin_access_key, admin_secret_key, username, secure=True):
    """
    Retrieve the access_key and secret_key for a specific user using the rgwadmin package.

    Parameters:
        host (str): The RGW admin host URL.
        admin_access_key (str): The admin access key for authentication.
        admin_secret_key (str): The admin secret key for authentication.
        username (str): The username of the user whose credentials are to be retrieved.
        secure (bool): Use HTTPS if True, otherwise HTTP.

    Returns:
        dict: A dictionary containing the user's access_key and secret_key, or None if not found.
    """
    try:
        # Initialize the RGWAdmin client
        rgw = RGWAdmin(
            access_key=admin_access_key,
            secret_key=admin_secret_key,
            server=host,
            secure=secure,
        )

        # Get user information
        user_info = rgw.get_user(username)
        return user_info

    except Exception as e:
        logging.error(f"An error occurred while retrieving user credentials: {e}")
        return None


def create_user(host, admin_access_key, admin_secret_key, user_info, secure=True):
    """
    Create a user and set their access_key and secret_key using the rgwadmin package.

    Parameters:
        host (str): The RGW admin host URL.
        admin_access_key (str): The admin access key for authentication.
        admin_secret_key (str): The admin secret key for authentication.
        user_info (dict): A dictionary containing all user attributes to recreate the user.
        secure (bool): Use HTTPS if True, otherwise HTTP.

    Returns:
        dict: The newly created user's details or None if the operation fails.
    """
    try:
        # Initialize the RGWAdmin client
        rgw = RGWAdmin(
            access_key=admin_access_key,
            secret_key=admin_secret_key,
            server=host,
            secure=secure,
        )

        # Create the user
        user = rgw.create_user(
            uid=user_info["user_id"],
            display_name=user_info["display_name"],
            access_key=quote(
                (
                    user_info["keys"][0]["access_key"]
                    if "keys" in user_info and user_info["keys"]
                    else None
                ),
                safe="",
            ),
            secret_key=quote(
                (
                    user_info["keys"][0]["secret_key"]
                    if "keys" in user_info and user_info["keys"]
                    else None
                ),
                safe="",
            ),
            max_buckets=user_info["max_buckets"],
        )
        return user

    except Exception as e:
        logging.error(f"An error occurred while creating the user: {e}")
        return None


def list_all_buckets(host, access_key, secret_key, secure=True):
    """
    List all buckets in the Ceph Object Storage using the rgwadmin package.

    Parameters:
        host (str): The RGW admin host URL.
        access_key (str): The access key for authentication.
        secret_key (str): The secret key for authentication.
        secure (bool): Use HTTPS if True, otherwise HTTP.

    Returns:
        list: A list of bucket names.
    """
    try:
        # Initialize the RGWAdmin client
        rgw = RGWAdmin(
            access_key=access_key, secret_key=secret_key, server=host, secure=secure
        )

        # Fetch the list of all buckets
        return rgw.get_bucket()

    except Exception as e:
        logging.error(f"An error occurred while listing buckets: {e}")
        return []


def get_bucket_owner(host, access_key, secret_key, bucket_name, secure=True):
    """
    Lists the bucket owner of a given bucketin in the Ceph Object Storage using the rgwadmin package.

    Parameters:
        host (str): The RGW admin host URL.
        access_key (str): The access key for authentication.
        secret_key (str): The secret key for authentication.
        bucket_name (str): The name of the bucket.
        secure (bool): Use HTTPS if True, otherwise HTTP.

    Returns:
        str: a username.
    """
    try:
        # Initialize the RGWAdmin client
        rgw = RGWAdmin(
            access_key=access_key, secret_key=secret_key, server=host, secure=secure
        )

        # Fetch the bucket owner
        bucket_info = rgw.get_bucket(bucket=bucket_name)
        return bucket_info["owner"]

    except Exception as e:
        logging.error(f"An error occurred while fetching bucket owner: {e}")
        return []
