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

# Read config file
with open("config.yaml") as file:
    config = yaml.safe_load(file)
    file.close()

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

# Function to get latest commit hash from master branch of repo from a project
def get_latest_commit_hash(baseURL, headers, projectKey, repo):
    latest_commit_hash = ""
    complete_url = "{}/rest/api/latest/projects/{}/repos/{}/commits?limit=1".format(baseURL, projectKey, repo)
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
    #authorization = str(base64.b64encode(bytes(':'+bb_pat, 'ascii')), 'ascii')
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer '+bb_pat
    }

    # Initializations
    project_list = json.loads(json.dumps(get_projects(baseURL, headers)['values']))

    project_keys = [dic['key'] for dic in project_list]
    debug(project_keys)

    project_repos = []
    project_count = 0
    all_repos_list = []
    commit_hash = ""

    info(f"Project_Key,Repo_Slug,Latest_Commit_Hash")
    
    for project in project_keys:
        repo_list = json.loads(json.dumps(get_repos(baseURL, headers, project)['values']))
        repo_slugs = [dic['slug'] for dic in repo_list]
        debug(repo_slugs)

        for repo in repo_slugs:
            commit_hash = get_latest_commit_hash(baseURL, headers, project, repo)
            info(f"{project},{repo},{commit_hash}")

        #all_repos_list.extend(project_repos)
        
        #project_count += 1
        #project_repos = []

        #debug(len(all_repos_list))

    #debug(f"All repos: {all_repos_list}")
    #total_repos = len(all_repos_list)
    #info(f"Number of repos: {total_repos}")

if __name__ == '__main__':
    args = parse_arguments()
    main()
