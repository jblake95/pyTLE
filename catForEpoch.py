"""
Obtain appropriate TLE catalogue for a desired epoch
"""

from tle import (
    parseEpochInput,
    getEpochCat,
    )
import json
import argparse as ap

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

def argParse():
    """
    Argument parser settings
    
    Parameters
    ----------
    None
    
    Returns
    -------
    args : array-like
        Array of command line arguments
    """
    parser = ap.ArgumentParser()
    
    parser.add_argument('run_path',
                        help='path to run catalogue json file',
                        type=str)
    
    parser.add_argument('out_dir',
                        help='output directory for resulting catalogue',
                        type=str)
    
    return parser.parse_args()

if __name__ == "__main__":
	
	args = argParse()
	
	try:
		with open(args.run_path, "r") as rc:
			run_cat = json.load(rc)
	except FileNotFoundError:
		print('No run catalogue found. Quitting...')
		quit()
	
	epoch = parseEpochInput(args)
	
	epoch_cat = getEpochCat(run_cat,
	                        epoch,
	                        args.out_dir)
