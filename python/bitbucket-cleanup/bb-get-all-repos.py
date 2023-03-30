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
import atlassian
from atlassian import Bitbucket
from pprint import pprint

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

# Function to log in to Bitbucket instance
def bitbucket_login(baseURL, username, password):
    bitbucket = Bitbucket(
        url = baseURL,
        username = username,
        password = password)

    return bitbucket

# Function to get all projects
def get_projects(baseURL, username, password):
    project_list = []
    try:
        bitbucket = bitbucket_login(baseURL, username, password)
    except Exception as err:
        debug(f"Unexpected {err=}, {type(err)=}")
        sys.exit()

    #pprint(list(bitbucket.project_list()))
    #pprint(bitbucket.project("VHRA"))

    for project in bitbucket.project_list():
        #print(str(project['key']))
        project_list.append(str(project['key']))

    return project_list

# Function to get repos from a project
def get_repos(baseURL, username, password, projectKey):
    repo_list = []
    try:
        bitbucket = bitbucket_login(baseURL, username, password)
    except Exception as err:
        debug(f"Unexpected {err=}, {type(err)=}")
        sys.exit()

    #pprint(list(bitbucket.repo_list(projectKey)))
    for repo in bitbucket.repo_list(projectKey):
            repo_list.append(str(repo['slug']))

    return repo_list

# Function to get latest commit hash from master branch of repo from a project
def get_latest_commit_hash(baseURL, username, password, projectKey, repo):
    latest_commit_hash = ""
    complete_url = "{}/rest/api/latest/projects/{}/repos/{}/commits?limit=1".format(baseURL, projectKey, repo)
    debug(complete_url)

    latest_commit_hash = call_url(complete_url, username, password)['values'][0]['id']

    return latest_commit_hash

# Function to call a request to a URL and return the response
def call_url(url, username, password):
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, auth=(username, password), headers=headers)
    if response.status_code == requests.codes.ok:
        return response.json()
    return ""


def main():
    pass

    username = args.username
    password = args.password
    baseURL = args.baseURL
    debug(f"Username is {username}, and Password is {password}")
    debug(f"Base URL is {baseURL}")

    # Initializations
    project_list = get_projects(baseURL, username, password)
    single_project = project_list[0]
    project_repos = []
    
    project_count = 0
    all_repos_list = []
    commit_hash = ""

    info(f"Project_Key,Repo_Slug,Latest_Commit_Hash")
    repo = get_repos(baseURL, username, password, single_project)[0]
    commit_hash = get_latest_commit_hash(baseURL, username, password, single_project, repo)
    
    for project in project_list:
        project_repos = get_repos(baseURL, username, password, project)
        for repo in project_repos:
            commit_hash = get_latest_commit_hash(baseURL, username, password, project, repo)
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
