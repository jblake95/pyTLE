"""
Obtain overall 3LE catalog for a given date range
"""

import argparse as ap
from spacetrack import SpaceTrackClient
import spacetrack.operators as op

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
    
    parser.add_argument('start',
                        help='start epoch, format YYYY-mm-ddTHH:MM:SS',
                        type=str)
    
    parser.add_argument('end',
                        help='end epoch, format YYYY-mm-ddTHH:MM:SS',
                        type=str)
    
    parser.add_argument('out_dir',
                        help='output directory for resulting catalog',
                        type=str)
    
    return parser.parse_args()

if __name__ == "__main__":
	
	
