#!/usr/local/bin/python
# File name: template.py
# Description: Basic format for Python scripts
# Author: Louis de Bruijn
# Created Date: 05-19-2020
# Stolen Date: 03-29-2023

# Import libraries here
import argparse
import sys
import logging
from logging import critical, error, info, warning, debug

# Define functions here

# Function to parse your arguments
def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(
        prog='name-of-program',
        description='Description of program')

    # Use argument to set logging level
    parser.add_argument('-v', metavar='verbosity', type=int, default=2,
        help='Verbosity of logging: 0 -critical, 1 -error, 2 -warning, 3 -info, 4 -debug')

    args = parser.parse_args()

    """Example help output
       usage: PythonScriptTemplate [-h] [-v verbosity]

       Arguments get parsed via --commands

       options:
         -h, --help    show this help message and exit
         -v verbosity  Verbosity of logging: 0 -critical, 1 -error, 2 -warning, 3 -info, 4 -debug"""

    # map argument to logging level
    verbose = {0: logging.CRITICAL, 1: logging.ERROR, 2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    # configure logging based on argument
    logging.basicConfig(format='%(message)s', level=verbose[args.v], stream=sys.stdout)

    return args

def main():
    pass

    info("This is the main program.")
    debug("This is a debug message.")

if __name__ == '__main__':
    args = parse_arguments()
    main()
