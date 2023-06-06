#!/Users/mboggess/.virtualenvs/bb/bin/python
# File Name: bb-get-all-repos.py
# Description: Return a CSV file with names of all project repos from a given BitBucket instance
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
import datetime

# Read config file
with open("config.yaml") as file:
    config = yaml.safe_load(file)
    file.close()

# Define functions here

# Function to parse your arguments
def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(
        prog='bb-get-all-project-repos',
        description='Return a CSV file with names of all project repos from a given BitBucket instance')

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
def get_projects(baseURL, headers):
    project_list = []

    complete_url = "{}/rest/api/1.0/projects?limit=300".format(baseURL)
    debug(complete_url)

    response = call_url(complete_url, headers)
    debug(response)

    return response

# Function to get repos from a project
def get_repos(baseURL, headers, projectKey):
    repo_list = []

    complete_url = "{}/rest/api/1.0/projects/{}/repos?limit=300".format(baseURL, projectKey)
    debug(complete_url)

    response = call_url(complete_url, headers)
    debug(response)

    return response

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
    #authorization = str(base64.b64encode(bytes(':'+bb_pat, 'ascii')), 'ascii')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+bb_pat
    }

    # Initializations
    project_list = json.loads(json.dumps(get_projects(baseURL, headers)['values']))

    project_keys = [dic['key'] for dic in project_list]

    info(f"Project_Key,Repo_Slug")
    
    for project in project_keys:
        repo_list = json.loads(json.dumps(get_repos(baseURL, headers, project)['values']))
        if not repo_list:
            info(f"{project},EmptyProject")
        else:
            repo_slugs = [dic['slug'] for dic in repo_list]

            for repo in repo_slugs:
                info(f"{project},{repo}")


if __name__ == '__main__':
    args = parse_arguments()
    main()
