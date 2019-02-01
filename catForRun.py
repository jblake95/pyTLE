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

TS = load.timescale()

SITE_LATITUDE = '28.7603135N'
SITE_LONGITUDE = '17.8796168W'
SITE_ELEVATION = 2387
TOPOS_LOCATION = Topos(SITE_LATITUDE, 
                       SITE_LONGITUDE, 
                       elevation_m=SITE_ELEVATION)

GEO_CHECK = ['g', 'geo']
LEO_CHECK = ['l', 'leo']
MEO_CHECK = ['m', 'meo']
HEO_CHECK = ['h', 'heo']
ALL_CHECK = ['a', 'all']

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

class Orbit:
    """
    Convenience class for orbit-specific searches
    """
    def __init__(self, orb_type):
        """
        Initiate Orbit object using SpaceTrack definitions
        
        Parameters
        ----------
        orb_type : str
            Desired type of orbit
            'g' - GEO
            'l' - LEO
            'm' - MEO
            'h' - HEO
            'a' - ALL
        """
        if orb_type.lower() in GEO_CHECK:
            self.eccentricity_lim = '<0.01'
            self.mean_motion_lim = '0.99--1.01'
        elif orb_type.lower() in LEO_CHECK:
            self.eccentricity_lim = '<0.25'
            self.mean_motion_lim = '>11.25'
        elif orb_type.lower() in MEO_CHECK:
            self.eccentricity_lim = '<0.25'
            self.period_lim = '600--800'
        elif orb_type.lower() in HEO_CHECK:
            self.eccentricity_lim = '>0.25'
        elif orb_type.lower() in ALL_CHECK:
            print('Full catalogue specified; no limits placed.')
        else:
            print('Please provide a valid orbit type\n'
                  'GEO - "g"\n'
                  'LEO - "l"\n'
                  'MEO - "m"\n'
                  'HEO - "h"\n'
                  'ALL - "a"\n')
            quit()

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
    
    def getPastCatGEO(self, start, end, out_dir=None, le_format='3le'):
        """
        Obtain catalog of GEO TLEs for a given epoch range
        
        Parameters
        ----------
        start, end : str
            Start and end epochs for search, format 'yyyy-mm-dd'
        out_dir : str, optional
            Output directory in which to store catalogue
            Default = None
        le_format : str
            Format of returned element sets ('tle' or '3le')
            Default = '3le'
        
        Returns
        -------
        tles : array-like
            Element sets returned from query to SpaceTrack
        """
        orb = Orbit('geo') 
        result = self.client.tle(iter_lines=True,
                                 eccentricity=orb.eccentricity_lim,
                                 mean_motion=orb.mean_motion_lim,
                                 epoch='{}--{}'.format(start, end),
                                 format=le_format)
        tles = [line for line in result]
        
        if out_dir is not None:
            with open(out_dir + 'run_catalogue.txt', 'w') as f:
                for line in tles:
                    f.write('{}\n'.format(line))
        
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
        self.obj = EarthSatellite(line1, line2, name)
        self.ts = TS
        
        self.eccentricity = float(self.line2[26:33])
        self.mean_motion = float(self.line2[52:63])
    
    def radec(self, epoch):
        """
        Determine radec coords for a given epoch
        """
        ra, dec, _ = (self.obj - self.obs).at(self.ts.utc(time)).radec()
        return ra._degrees * u.degree, dec.degrees * u.degree

#class Catalog:
    #"""
    #TLE catalog
    #"""
    #def __init__(self, tles):   
        #    

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

if __name__ == "__main__":
    
    args = argParse()
    
    st = ST() # connect to SpaceTrack
    
    cat = st.getPastCatGEO(args.start,
                            args.end,
                            args.out_dir)
    print(len(cat))
    
    
