#!/usr/bin/env python

import logging


def write_rclone_config(
    file_path, connection_name, access_key, secret_access_key, endpoint
):
    """
    Appends an rclone configuration command to a file with the specified options.

    :param file_path: Path to the file where the command will be appended.
    :param connection_name: Name of the rclone connection.
    :param access_key: Access key for the configuration.
    :param secret_access_key: Secret access key for the configuration.
    :param endpoint: Endpoint for the configuration.
    """
    command = (
        f"rclone config create {connection_name} s3 provider Ceph "
        f"access_key_id {access_key} secret_access_key {secret_access_key} "
        f"endpoint {endpoint} acl public-read"
    )

    try:
        with open(file_path, "a") as file:
            file.write(command + "\n")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
