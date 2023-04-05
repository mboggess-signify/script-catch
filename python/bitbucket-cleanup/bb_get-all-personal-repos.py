#!/Users/mboggess/.virtualenvs/bb/bin/python
# File Name: bb-get-all-repos.py
# Description: Return a CSV file with names of all personal repos from a given BitBucket instance
# Author: Megan Boggess
# Created Date: 03-29-2023

# Import libraries here
import argparse
import sys
import logging
from logging import critical, error, info, warning, debug
import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import pprint
import base64
import csv
import os
import yaml

# Read config file
with open("config.yaml") as file:
    config = yaml.safe_load(file)
    file.close()

# Define functions here

# Function to parse your arguments
def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(
        prog='bb-get-all-personal-repos',
        description='Return a CSV file with names of all personal repos from a given BitBucket instance')

    # Use argument to set logging level
    parser.add_argument('-v', '--verbosity', metavar='\b', type=int, default=2,
        help='verbosity of logging: 0 -critical, 1 -error, 2 -warning, 3 -info, 4 -debug')

    # Use argument to set password
    parser.add_argument('-p', '--pat', metavar='\b', type=str, required=True,
        help='personal access token of user to access BitBucket instance')

    args = parser.parse_args()

    # Map argument to logging level
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    # Configure logging based on argument
    logging.basicConfig(format='%(message)s', level=verbose[args.verbosity], stream=sys.stdout)

    return args

# Function to get all projects
def get_users(baseURL, headers, limit, start):

    if start == 0:
        complete_url = "{}/rest/api/1.0/users?limit={}".format(baseURL, limit, start)
    else:
        complete_url = "{}/rest/api/1.0/users?limit={}&start={}".format(baseURL, limit, start)
    debug(complete_url)

    response = call_url(complete_url, headers)
    debug(response)

    return response

# Function to get repos from a project
def get_repos(baseURL, headers, user_slug):

    complete_url = "{}/rest/api/1.0/users/{}/repos?limit=1000".format(baseURL, user_slug)
    debug(complete_url)

    try:
        response = call_url(complete_url, headers)
    except Error as err:
        debug(f"Unexpected {err=}, {type(err)=}")
        debug(f"{response}")
        response = []

    debug(response)
    return response

# Function to get latest commit hash from master branch of repo from a project
def get_latest_commit_hash(baseURL, headers, user_slug, repo):
    latest_commit_hash = ""
    complete_url = "{}/rest/api/1.0/users/{}/repos/{}/commits?limit=1".format(baseURL, user_slug, repo)
    debug(complete_url)

    response = call_url(complete_url, headers)

    try:
        latest_commit_hash = response['values'][0]['id']
    except TypeError as err:
        debug(f"Unexpected {err=}, {type(err)=}")
        debug(f"{response}")
        debug("Probably no master branch")
        latest_commit_hash = "NoMaster"
    except IndexError as err:
        debug(f"Unexpected {err=}, {type(err)=}")
        debug(f"{response}")
        debug("Probably empty repo")
        latest_commit_hash = "EmptyRepo"
    except Exception as err:
        debug(f"Unexpected {err=}, {type(err)=}")
        debug(f"{response}")
        latest_commit_hash = None

    return latest_commit_hash

# Function to call a request to a URL and return the response
def call_url(url, headers):
    headers = headers
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.ok:
        return response.json()
    return response.status_code


def main():
    pass

    bb_pat = args.pat
    baseURL = config['bitbucket_base_url']
    debug(f"Base URL is {baseURL}")

    # Define headers for API calls
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+bb_pat
    }

    # Initializations
    user_list = []
    limit = 1000
    start = 0

    is_end = json.dumps(get_users(baseURL, headers, limit, start)['isLastPage'])
    debug(is_end)

    while is_end != "true":
        user_list.append(json.loads(json.dumps(get_users(baseURL, headers, limit, start)['values'])))

        start = limit
        limit = limit + 1000
        is_end = json.dumps(get_users(baseURL, headers, limit, start)['isLastPage'])

    flat_user_list = [ item for sublist in user_list for item in sublist ]
    debug(flat_user_list)
    
    user_names = [dic['slug'] for dic in flat_user_list]
    debug(user_names)

    info(f"User_Name,Repo_Slug,Latest_Commit_Hash")
    
    for user in user_names:
        try:
            repo_list = json.loads(json.dumps(get_repos(baseURL, headers, user)['values']))
            repo_slugs = [dic['slug'] for dic in repo_list]
        except:
            repo_slugs = []
            pass

        for repo in repo_slugs:
            commit_hash = get_latest_commit_hash(baseURL, headers, user, repo)
            info(f"{user},{repo},{commit_hash}")


if __name__ == '__main__':
    args = parse_arguments()
    main()
