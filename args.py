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

    return parser.parse_args(args)
