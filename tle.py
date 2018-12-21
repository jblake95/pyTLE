"""
Useful functions for dealing with Space-Track two-line elements
"""

from spacetrack import SpaceTrackClient
import spacetrack.operators as op

def getSatCat(name, pw, epoch='>now-30', le_format='3le', save=True):
    """
    Retrieves full catalogue of latest elsets in requested format
    
    Parameters
    ----------
    name : str
        Username for access to the Space-Track database
    pw : str
        Password for access to the Space-Track database
    epoch : str, optional
        Dates from which to pull elsets. Can specify a period of time
        using '--', for example '2017-01-01--2017-12-08', will give 
        elsets that have updated within that epoch range
        Default = '>now-30' (for latest elsets)
    le_format : str
        Format of the retrieved line element sets
        'tle' - returns two line elements
        '3le' - returns three line elements (includes sat names)
        Default = '3le'
    save : bool, optional
        Toggle to save catalogue to file
        Default = True
    
    Returns
    -------
    None
    """ 
    st = SpaceTrackClient(identity=name, password=pw)
    
    cat = st.tle_latest(iter_lines=True, 
                        epoch=epoch, 
                        ordinal=1, 
                        format=le_format)
    
    if save:
		with open('tle_latest.txt', 'w') as f:
			for line in data:
				f.write(line + '\n')
    
    return cat

def getTLE(norad_id, epoch):
	"""
	Obtain a TLE for a given object within a desired epoch range
	"""
	st.tle(norad_cat_id=25544, orderby='epoch desc', limit=22, format='tle')
	
	return tle
