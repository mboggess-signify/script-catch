#!/Users/mboggess/.virtualenvs/bb/bin/python
# File Name: bb-get-all-repos.py
# Description: Return a CSV file with names of all repos from a given BitBucket instance
# Author: Megan Boggess
# Created Date: 03-29-2023

# Import libraries here
import argparse
import sys
import logging
from logging import critical, error, info, warning, debug
import requests
from requests.auth import HTTPBasicAuth

# Define functions here

# Function to parse your arguments
def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(
        prog='bb-get-all-repos',
        description='Return a CSV file with names of all repos from a given BitBucket instance')

    # Use argument to set logging level
    parser.add_argument('-v', '--verbosity', metavar='\b', type=int, default=2,
        help='verbosity of logging: 0 -critical, 1 -error, 2 -warning, 3 -info, 4 -debug')

    # Use argument to set username
    parser.add_argument('-u', '--username', metavar='\b', type=str, required=True,
        help='username of user to access BitBucket instance')

    # Use argument to set password
    parser.add_argument('-p', '--password', metavar='\b', type=str, required=True,
        help='password of user to access BitBucket instance')

    # Use argument to set base URL
    parser.add_argument('-b', '--baseURL', metavar='\b', type=str, required=True,
        help='base URL to BitBucket instance')

    args = parser.parse_args()

    # Map argument to logging level
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    # Configure logging based on argument
    logging.basicConfig(format='%(message)s', level=verbose[args.verbosity], stream=sys.stdout)

    return args

def main():
    pass

    username = args.username
    password = args.password
    debug(f"Username is {username}, and Password is {password}")
    baseURL = args.baseURL
    debug(f"Base URL is {baseURL}")

if __name__ == '__main__':
    args = parse_arguments()
    main()
