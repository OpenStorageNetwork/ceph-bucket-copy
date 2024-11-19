#!/usr/bin/env python

import argparse


def args(args):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--credentials",
        dest="credentials_file",
        help="File containing the credentials for the OSN pod.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--buckets",
        dest="buckets_file",
        help="File containing the list of buckets to copy.",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--config-commands-file",
        dest="config_commands_file",
        help="File to write the rclone configuration commands.",
        type=str,
        default="config_commands.sh",
        required=False,
    )

    parser.add_argument(
        "--copy-commands-file",
        dest="copy_commands_file",
        help="File to write the rclone copy commands.",
        type=str,
        default="copy_commands.sh",
        required=False,
    )

    return parser.parse_args(args)
