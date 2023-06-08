#!/Users/mboggess/.virtualenvs/bb/bin/python3
# File Name: bamboo_get-all-project-deploy-results.py
# Description: Return a CSV file with details of all project deploy results from a given Bamboo instance
# Author: Megan Boggess
# Created Date: 06-08-2023

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
with open("config_bamboo.yaml") as file:
    config = yaml.safe_load(file)
    file.close()

# Define functions here

# Function to parse your arguments
def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(
        prog='bamboo_get-all-project-deploy-results',
        description='Return a CSV file with details of all project deploy results from a given Bamboo instance')

    # Use argument to set logging level
    parser.add_argument('-v', '--verbosity', metavar='\b', type=int, default=2,
        help='verbosity of logging: 0 -critical, 1 -error, 2 -warning, 3 -info, 4 -debug')

    # Use argument to set password
    parser.add_argument('-p', '--pat', metavar='\b', type=str, required=True,
        help='personal access token of user to access Bamboo instance')

    args = parser.parse_args()

    # Map argument to logging level
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    # Configure logging based on argument
    logging.basicConfig(format='%(message)s', level=verbose[args.verbosity], stream=sys.stdout)

    return args

# Function to get all projects
def get_projects(baseURL, headers):
    complete_url = "{}/rest/api/latest/project?showEmpty=true".format(baseURL)
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
    baseURL = config['bamboo_base_url']
    debug(f"Base URL is {baseURL}")

    # Define headers for API calls
    #authorization = str(base64.b64encode(bytes(':'+bb_pat, 'ascii')), 'ascii')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+bb_pat
    }

    # Initializations
    project_list = []
    project_keys = []

    # Get Projects
    project_list = json.loads(json.dumps(get_projects(baseURL, headers)['projects']['project']))
    debug(project_list)

    project_keys = [dic['key'] for dic in project_list]
    debug(project_keys)

    # Print header for csv file
    info(f"Project_Key,Project_Plan,Latest_Build_Date")

#    for key in project_keys:
        # Get each project's deploys

        # Get each deploy's details

#        for x in y:
            # Get each deploy's completed date

            # Print data to csv file


if __name__ == '__main__':
    args = parse_arguments()
    main()
