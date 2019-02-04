"""
Obtain overall 3LE catalog for a given date range
"""

from tle import TLE, ST
import json
import datetime
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

def getEpochCat(run_cat, epoch, out_dir):
    """
    Refine a run catalogue, keeping only latest element sets with 
    respect to the desired epoch
    """
    i = 0
    epoch_cat = []
    tracker = {}
    while i < len(run_cat):
        print(i)
        tle = TLE(run_cat[i+1], run_cat[i+2], name=run_cat[i])
        if tle.norad_id in tracker.keys():
            tracker[tle.norad_id].append([tle.line1,
                                          tle.line2])
        else:
            tracker.update({tle.norad_id:[[tle.line1,
                                           tle.line2]]})
        i += 3
    
    print(tracker)
    
    with open(out_dir + 'test.json', 'w') as f:
        json.dump(tracker, f)
    
    return epoch_cat

if __name__ == "__main__":
    
    args = argParse()
    
    st = ST() # connect to SpaceTrack
    
    run_cat = st.getRunCatGEO(args.start,
                              args.end)
                              #args.out_dir)
    
    print(len(run_cat))
    
    epoch_cat = getEpochCat(run_cat, 'blah', args.out_dir) 
