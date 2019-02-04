"""
Obtain overall 3LE catalog for a given date range
"""

from tle import (
    TLE, 
    ST,
    )
from datetime import (
    datetime,
    timedelta,
    )
import json
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
    
    parser.add_argument('start',
                        help='start epoch, format YYYY-mm-dd',
                        type=str)
    
    parser.add_argument('end',
                        help='end epoch, format YYYY-mm-dd',
                        type=str)
    
    parser.add_argument('out_dir',
                        help='output directory for resulting catalog',
                        type=str)
    
    return parser.parse_args()

def parseInput(args):
    """
    Read the input arguments in a more useful format
    
    Parameters
    ----------
    args : argparse object
        Arguments returned by argparse user interaction
    
    Returns
    -------
    start_date, end_date : datetime objects
        Start and end dates of run in datetime format
    """
    try:
        start_date = datetime.strptime(args.start, '%Y-%m-%d')
        end_date = datetime.strptime(args.end, '%Y-%m-%d')
    except:
        print('Incorrect format: please supply dates "YYYY-mm-dd"...')
        quit()
    
    return start_date, end_date

def getYearDay(epoch):
    """
    Convert a datetime object to day of the year
    
    Parameters
    ----------
    epoch : datetime object
        Epoch to convert to year day
    
    Returns
    -------
    yday : float
        Corresponding year day
    """
    return epoch.timetuple().tm_yday

def organiseCat(cat, out_dir):
    """
    Organise run catalogue, grouping tles by norad id in a 
    user-friendly format
    
    Parameters
    ----------
    cat : array-like
        List of 3les pulled from the Space-Track database between the
        desired start and end dates
    out_dir : str
        Directory in which to store output json file containing
        organised version of the run catalogue
    
    Returns
    -------
    org_cat : dict
        Run catalogue organised by norad id
    """
    i = 0
    org_cat = {}
    while i < len(cat):
        print('Processing {}/{}'.format(str(i),str(len(cat))), end="\r")
        tle = TLE(cat[i+1], cat[i+2], name=cat[i])
        if tle.norad_id in org_cat.keys():
            org_cat[tle.norad_id].append([tle.line1,
                                          tle.line2])
        else:
            org_cat.update({tle.norad_id:[[tle.line1,
                                           tle.line2]]})
        i += 3
    
    with open(out_dir + 'run_cat.json', 'w') as f:
        json.dump(org_cat, f)
    
    return org_cat

if __name__ == "__main__":
    
    args = argParse()
    
    # connect to SpaceTrack and obtain catalogue for INT run
    st = ST()
    run_cat = st.getRunCatGEO(args.start,
                              args.end,
                              args.out_dir)
    
    # organise resulting catalogue into user-friendly format
    epoch_cat = organiseCat(run_cat, args.out_dir) 
