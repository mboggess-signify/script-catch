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

# Function to get all deployment projects
def get_deployment_projects(baseURL, headers):
    complete_url = "{}/rest/api/latest/deploy/project/all".format(baseURL)
    debug(complete_url)

    response = call_url(complete_url, headers)
    debug(response)

    return response


# Function to get deployment project's dashboard
def get_deployment_project_dashboard(baseURL, headers, deployment_project_id):
    complete_url = "{}/rest/api/latest/deploy/dashboard/{}".format(baseURL, deployment_project_id)
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
    deployment_project_list = []
    deployment_project_ids = []
    deployment_project_names = []
    deployment_project_details = {}

    # Get Deployment Projects
    deployment_project_list = json.loads(json.dumps(get_deployment_projects(baseURL, headers)))
    debug(deployment_project_list)

    deployment_project_ids = [dic['id'] for dic in deployment_project_list]
    debug(deployment_project_ids)

    deployment_project_names = [dic['name'] for dic in deployment_project_list]
    debug(deployment_project_names)

    deployment_project_details = {deployment_project_ids[i]: deployment_project_names[i] for i in range(len(deployment_project_ids))}
    debug(deployment_project_details)

    # Print header for csv file
    info(f"DeploymentProjectName, EnvironmentName, LastEnvironmentDeployDate")

    for dp_id in deployment_project_ids:
        # Get each project's deploy dashboard
        deployment_project_dashboard = json.loads(json.dumps(get_deployment_project_dashboard(baseURL, headers, dp_id)[0]))
        debug(deployment_project_dashboard)
        debug(type(deployment_project_dashboard))
        debug(deployment_project_dashboard.keys())

        dp_name = deployment_project_details[dp_id]
        debug(dp_name)

        # Check if environmentStatuses array exists
        # If so, there is environment data
        # If not, there is no environment data, so can just say "No environments"
        envStatusCheck = deployment_project_dashboard.get('environmentStatuses')
        debug(type(envStatusCheck))
        debug(envStatusCheck)
        
        if envStatusCheck is not None:
            debug(f"There are environment deploys!")

            deploy_results_check_key = "deploymentResult"
            environment_name = ""
            environment_last_deploy_epoch = ""
            environment_last_deploy_date = ""

            for environment in envStatusCheck:
                if deploy_results_check_key in environment:
                    environment_name = environment['environment']['name']
                    environment_last_deploy_epoch = environment['deploymentResult']['finishedDate']
                    environment_last_deploy_date = datetime.datetime.fromtimestamp(environment_last_deploy_epoch/1000)
                    debug(f"There are deployment results for {environment_name}!")
                else:
                    environment_name = environment['environment']['name']
                    environment_last_deploy_date = "N/A"
                    debug(f"There are no deploys for {environment_name}")

                info(f"{dp_name}, {environment_name}, {environment_last_deploy_date}")
        else:
            debug(f"There were never environment deploys!")
            environment_name = "None"
            environment_last_deploy_date = "N/A"
            info(f"{dp_name}, {environment_name}, {environment_last_deploy_date}")


            # Print data to csv file


if __name__ == '__main__':
    args = parse_arguments()
    main()
