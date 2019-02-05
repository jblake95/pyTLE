"""
Obtain overall 3le catalog for a given epoch range
"""

from tle import (
    TLE, 
    ST,
    parseRunInput,
    checkRunLength,
    organiseCat,
    )
import argparse as ap
from datetime import timedelta

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
                        help='start epoch, format YYYY-mm-dd',
                        type=str)
    
    parser.add_argument('end',
                        help='end epoch, format YYYY-mm-dd',
                        type=str)
    
    parser.add_argument('cat_type',
                        help='type of objects to query; \n'
                             'GEO - "g", \n'
                             'LEO - "l", \n'
                             'MEO - "m", \n'
                             'HEO - "h", \n'
                             'ALL - "a"  \n',
                        type=str)
    
    parser.add_argument('out_dir',
                        help='output directory for resulting catalog',
                        type=str)
    
    return parser.parse_args()

if __name__ == "__main__":
    
    args = argParse()
    
    start, end = parseRunInput(args)
    
    # adjust dates for leniency
    start -= timedelta(days=30) # match usual allowance for Space-Track
    end += timedelta(days=5)    # future tle better than very old tle
    
    # check length of run does not exceed limit for catalogue type
    dates = checkRunLength(start, end, args.cat_type)
    
    # connect to SpaceTrack and obtain catalogue for INT run
    st = ST()
    run_cat = st.getRunCat(dates,
                           args.cat_type,
                           args.out_dir)
    
    # organise resulting catalogue into user-friendly format
    epoch_cat = organiseCat(run_cat, args.out_dir) 
