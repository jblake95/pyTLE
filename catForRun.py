"""
Obtain overall 3LE catalog for a given date range
"""

import argparse as ap
import getpass as gp
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

class ST:
	"""
	Space-Track Interface
	"""
	def __init__(self):
		un, pw = self.requestAccess()
		self.username = un
		self.password = pw
		self.client = SpaceTrackClient(identity=un, password=pw)
	
	def requestAccess(self):
		"""
		Obtain user access details
		"""
		st_un = 'J.Blake@warwick.ac.uk'
		st_pw = gp.getpass('Space-Track password: ')
		return st_un, st_pw
	
	def getLatestCatalog(self, out_dir=None, le_format='3le'):
		"""
		Obtain catalog of latest TLEs from Space-Track
		"""
		return self.client.tle_latest(iter_lines=True, 
                                      epoch='>now-30', 
                                      ordinal=1, 
                                      format=le_format)
    
    def getPastCatalog(self, start, end, out_dir=None, le_format='3le'):
		"""
		Obtain catalog of TLEs for a given epoch range
		"""
		
		return self.client.tle_latest(iter_lines=True, 
                                      epoch='>now-30', 
                                      ordinal=1, 
                                      format=le_format)

class TLE:
	"""
	Two Line Element
	"""

if __name__ == "__main__":
	
	#args = argParse()
	
	st = ST()
	print(st.client)
	
	cat = st.getLatestCatalog(le_format='3le')
	
	for c in cat:
		print(c)
	
	
