"""
Obtain overall 3LE catalog for a given date range
"""

import argparse as ap
import getpass as gp
from spacetrack import SpaceTrackClient
import spacetrack.operators as op
import datetime
from skyfield.api import load, Topos, utc
from skyfield.sgp4lib import EarthSatellite

SITE_LATITUDE = '28.7603135N'
SITE_LONGITUDE = '17.8796168W'
SITE_ELEVATION = 2387
TOPOS_LOCATION = Topos(SITE_LATITUDE, 
                       SITE_LONGITUDE, 
                       elevation_m=SITE_ELEVATION)

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
	
	def getLatestTLE(self, norad, le_format='3le'):
		"""
		Obtain latest TLE for a NORAD object
		"""
		return self.client.tle_latest(norad_cat_id=norad,
		                              iter_lines=True,
		                              ordinal=1,
		                              format=le_format)
	
	def getLatestCatalog(self, out_dir=None, le_format='3le'):
		"""
		Obtain catalog of latest TLEs from Space-Track
		"""
		return self.client.tle_latest(iter_lines=True, 
                                      epoch='>now-30', 
                                      ordinal=1, 
                                      format=le_format)
    
    def getPastTLE(self, norad, start, end, epoch=None, le_format='3le'):
		"""
		Obtain list of TLEs for a NORAD object within an epoch range,
		narrowed down to one (most recent) if desired epoch given
		"""
		
		
		return
    
    def getPastCatalog(self, start, end, out_dir=None, le_format='3le'):
		"""
		Obtain catalog of TLEs for an epoch range
		"""
		tles = []
		# NORAD ids go up to around 90000 for full catalogue
		for idx in range(100000):
			result = self.client.tle(norad_cat_id=i,
			                         iter_lines=True,
			                         epoch='{}--{}'.format(start, end),
			                         format=le_format)
			obj_tles = [line for line in result]
			if len(tle) > 0:
				# check if GEO
				testcase = TLE(obj_tles[1], obj_tles[2], obj_tles[0])
				if abs(testcase.mean_motion-1) < 0.01 and \
				                      testcase.eccentricity < 0.01:
					tles += obj_tles
				else:
					continue
		
		if out_dir is not None:
			with open(out_dir + 'run_catalogue.txt', 'w') as cat:
				for line in tles:
					cat.write('{}\n'.format(line))
		
		return tles

class TLE:
	"""
	Two Line Element
	"""
	def __init__(self, line1, line2, name=None):
		self.line1 = line1
		self.line2 = line2
		if name is not None:
			self.name = name
		
		self.obs = TOPOS_LOCATION
        self.obj = EarthSatellite(tle_array[1], tle_array[2])
        self.ts = load.timescale()
        
        self.eccentricity = self.line2[26:33]
        self.mean_motion = self.line2[52:63]
	
	def radec(self, epoch):
		"""
		Determine radec coords for a given epoch
		"""
		ra, dec, _ = (self.obj - self.obs).at(self.ts.utc(time)).radec()
        return ra._degrees * u.degree, dec.degrees * u.degree

class Catalog:
	"""
	TLE catalog
	"""
	def __init__(self, tles):	
		

def getYearDay():
	"""
	Convert a datetime object to day of the year
	"""
	
	
	return yearday

if __name__ == "__main__":
	
	#args = argParse()
	
	
	tle = TLE()
	
	
