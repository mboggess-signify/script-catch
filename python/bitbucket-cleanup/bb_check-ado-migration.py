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
        prog='bb_check-ado-migration',
        description='Return a CSV file with names of all repos from a given BitBucket instance and whether they have been migrated to ADO or not')

    # Use argument to set logging level
    parser.add_argument('-v', '--verbosity', metavar='\b', type=int, default=2,
        help='verbosity of logging: 0 -critical, 1 -error, 2 -warning, 3 -info, 4 -debug')

    # Use argument to set PAT
    parser.add_argument('-p', '--pat', metavar='\b', type=str, required=True,
        help='personal access token (PAT) of user to access ADO instance')

    args = parser.parse_args()

    # Map argument to logging level
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    # Configure logging based on argument
    logging.basicConfig(format='%(message)s', level=verbose[args.verbosity], stream=sys.stdout)

    return args

# Function to call a request to a URL and return the response
def call_url(url, headers):
    headers = headers
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.ok:
        return response.json()
    return ""

# Function to get all ADO repos from HCC project
def get_all_repos(org_url, headers, api_version):
    complete_url = "{}/HCC/_apis/git/repositories?api-version={}".format(
        org_url,api_version)
    debug(complete_url)

    response = call_url(complete_url, headers)

    return response

# Function to search an ADO repo for a specific commit ID
def search_repo_for_commit_id(headers, org_url, ado_project, ado_repo, bb_commit_id, api_version):
    complete_url = "{}/{}/_apis/git/repositories/{}/commits?searchCriteria.ids={}&api-version={}".format(
        org_url, ado_project, ado_repo, bb_commit_id, api_version)
    debug(complete_url)

    response = call_url(complete_url, headers)

    return response

def main():
    pass

    personal_access_token = args.pat
    ado_base_url = config['ado_base_url']
    ado_api_version = config['ado_api_version']
    ado_project = config['ado_project']
    bb_repo_file = config['bb_repo_csv']

    # Define headers for API calls
    authorization = str(base64.b64encode(bytes(':'+personal_access_token, 'ascii')), 'ascii')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic '+authorization
    }

    # Get all ADO repos (just one org: "HCC", no projects?) as a json array
    ado_repos = json.loads(json.dumps(get_all_repos(ado_base_url, headers, ado_api_version)['value']))
    debug(ado_repos)
    ado_repo_names = [dic['name'] for dic in ado_repos]
    debug(ado_repo_names)

    # Load csv of Bitbucket repos
    info("BB_REPO,BB_COMMIT_ID,MIGRATED_ADO_REPO")

    with open(bb_repo_file, newline='\n') as csvfile:
        reporeader = csv.reader(csvfile, delimiter=',')
        next(reporeader)

        for row in reporeader:
            debug(row)
            bb_repo = row[1]
            bb_commit_id = row[2]

            for ado_repo in ado_repo_names:
                migrated = ""
                debug(f"{bb_repo}, {bb_commit_id}, {ado_repo}")
                search_response = json.loads(json.dumps(search_repo_for_commit_id(
                    headers, ado_base_url, ado_project, ado_repo, bb_commit_id, ado_api_version)))
                debug(search_response)

                if search_response == "":
                    migrated = "NotMigrated"
                    debug(search_response)
                elif search_response["count"] == 1:
                    migrated = ado_repo
                    break
                else:
                    migrated = "NotMigrated"
                    debug(search_response)

            info(f"{bb_repo},{bb_commit_id},{migrated}")

if __name__ == '__main__':
    args = parse_arguments()
    main()
