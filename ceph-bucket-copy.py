#!/usr/bin/env python

import args
import s3_buckets
import radosgw_admin
import write_commands
import sys
import yaml
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Example usage
if __name__ == "__main__":

    # Parse the command line arguments
    args = args.args(sys.argv[1:])

    # Read the configuration file
    credentials = yaml.safe_load(open(args.credentials_file))
    buckets = yaml.safe_load(open(args.buckets_file))

    for bucket_name, bucket_info in buckets.items():
        source = bucket_info["source"]
        destination = bucket_info["destination"]
        bucket_owner = radosgw_admin.get_bucket_owner(
            source,
            credentials[source]["access_key"],
            credentials[source]["secret_key"],
            bucket_name,
            secure=True,
        )
        logging.info(
            f"Bucket: {bucket_name}, BucketOwner: {bucket_owner}, Source: {source}, Destination: {destination}"
        )

        # Get the list of users
        s = radosgw_admin.list_all_users(
            source,
            credentials[source]["access_key"],
            credentials[source]["secret_key"],
            secure=True,
        )
        d = radosgw_admin.list_all_users(
            destination,
            credentials[destination]["access_key"],
            credentials[destination]["secret_key"],
            secure=True,
        )

        # Get users that start with bucket_name
        source_users = [item for item in s if item.startswith(bucket_name)]
        destination_users = [item for item in d if item.startswith(bucket_name)]

        # Check if there are any users that start with the bucket_name
        if len(source_users) == 0:
            logging.warning(f"No users found on {source} starting with {bucket_name}.")
        else:

            # Add the source users to the destination
            for source_user in source_users:
                # Check if the user already exists in the destination
                if source_user in destination_users:
                    logging.info(f"User {source_user} already exists on {destination}.")

                    #
                    # If the user exists, do we want to update the keys or leave them as is?
                    #

                else:
                    # Get the source user credentials
                    source_user_info = radosgw_admin.get_user(
                        source,
                        credentials[source]["access_key"],
                        credentials[source]["secret_key"],
                        source_user,
                        secure=True,
                    )

                    if source_user_info:
                        # Create the user in the destination
                        radosgw_admin.create_user(
                            destination,
                            credentials[destination]["access_key"],
                            credentials[destination]["secret_key"],
                            source_user_info,
                            secure=True,
                        )
                        logging.info(f"User {source_user} created on {destination}.")
                    else:
                        logging.error(
                            f"User {source_user} has no credentials on {source}."
                        )

        # Get the list of buckets
        s = radosgw_admin.list_all_buckets(
            source,
            credentials[source]["access_key"],
            credentials[source]["secret_key"],
            secure=True,
        )
        d = radosgw_admin.list_all_buckets(
            destination,
            credentials[destination]["access_key"],
            credentials[destination]["secret_key"],
            secure=True,
        )

        if bucket_name not in s:
            logging.warning(f"Bucket {bucket_name} not found on {source}.")
            continue

        if bucket_name in d:
            logging.warning(f"Bucket {bucket_name} already exists on {destination}.")

            #
            # If bucket exists, do we want to update the bucket policy or leave it as is?
            #

            continue
	# Get the bucket owner credentials
        bucket_owner_info = radosgw_admin.get_user(
            source,
            credentials[source]["access_key"],
            credentials[source]["secret_key"],
            bucket_owner,
            secure=True,
	)
        # Get the source bucket policy
        source_bucket_policy = s3_buckets.get_bucket_policy(
            source,
            bucket_owner_info["keys"][0]["access_key"],
            bucket_owner_info["keys"][0]["secret_key"],
            bucket_name,
        )

        # Create the bucket on the destination
        s3_buckets.create_bucket(
            destination,
            credentials[destination]["access_key"],
            credentials[destination]["secret_key"],
            bucket_name,
            region=None,
        )

        # Set the bucket policy on the destination
        if source_bucket_policy:
            policy_result = s3_buckets.set_bucket_policy(
                destination,
                credentials[destination]["access_key"],
                credentials[destination]["secret_key"],
                bucket_name,
                source_bucket_policy,
            )
            if policy_result:
                logging.info(f"Bucket policy set for {bucket_name} on {destination}.")
        else:
            logging.warning(f"No bucket policy found for {bucket_name} on {source}.")

        # Write the rclone configuration command
        write_commands.write_rclone_config(
            args.config_commands_file,
            f"{bucket_name}_source",
            (
                source_user_info["keys"][0]["access_key"]
                if "keys" in source_user_info and source_user_info["keys"]
                else None
            ),
            (
                source_user_info["keys"][0]["secret_key"]
                if "keys" in source_user_info and source_user_info["keys"]
                else None
            ),
            f"https://{source}",
        )

        write_commands.write_rclone_config(
            args.config_commands_file,
            f"{bucket_name}_destination",
            (
                source_user_info["keys"][0]["access_key"]
                if "keys" in source_user_info and source_user_info["keys"]
                else None
            ),
            (
                source_user_info["keys"][0]["secret_key"]
                if "keys" in source_user_info and source_user_info["keys"]
                else None
            ),
            f"https://{destination}",
        )

        logging.info(f"Wrote rclone config commands to {args.config_commands_file}.")

        write_commands.write_rclone_copy(
            args.copy_commands_file,
            f"{bucket_name}_source",
            f"{bucket_name}_destination",
            bucket_name,
        )

        logging.info(f"Wrote rclone copy commands to {args.copy_commands_file}.")
