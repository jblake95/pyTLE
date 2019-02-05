"""
Obtain appropriate TLE catalogue for a desired epoch
"""

import argparse as ap

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
	
	
