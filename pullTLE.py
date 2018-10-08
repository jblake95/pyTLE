#!/usr/bin/env python2.7
"""
Pulls latest elsets from Space-Track
"""

from spacetrack import SpaceTrackClient
import datetime
from os.path import realpath, dirname, isdir
from os import mkdir

### user can set their login details as default ###
def getSatCat(name='', pw='',
              le_format='3le'):
    """
    Retrieves full catalog of latest elsets in requested format
    
    Parameters
    ----------
    name : str
        Username for access to the Space-Track database
        Default = '' 
    pw : str
        Password for access to the Space-Track database
        Default = ''
    le_format : str
        Format of the retrieved line element sets
        'tle' - returns two line elements
        '3le' - returns three line elements (includes sat names)
        Default = '3le'
    
    Returns
    -------
    None
    
    Raises
    ------
    None
    """ 
    st = SpaceTrackClient(identity=name, password=pw)
    
    data = st.tle_latest(iter_lines=True, epoch='>now-30', ordinal=1, format=le_format)
    
    # get datestamp
    date = datetime.datetime.now()
    date_str = date.strftime('%Y%m%d')
    mth = str(date.month) + '/'
    yr = str(date.year) + '/'
    
    # get filepath
    filepath = dirname(realpath(__file__)) + '/'
    
    if not isdir(filepath + yr):
        mkdir(filepath + yr)
    
    if not isdir(filepath + yr + mth):
        mkdir(filepath + yr + mth)
    
    with open(filepath + yr + mth + '/tle_' + date_str + '.txt', 'w') as f:
        for line in data:
            f.write(line + '\n')
    
    return None

if __name__ == "__main__":
    
    # pull sat 3les from Space-Track
    getSatCat()
