"""
Module for dealing with Space-Track elsets
"""

import getpass as gp
from spacetrack import SpaceTrackClient
import spacetrack.operators as op
from skyfield.api import load, Topos, utc
from skyfield.sgp4lib import EarthSatellite

TS = load.timescale() # save repeated use in iterative loops
LE_FORMAT = '3le'     # TODO: generalise to allow for 'tle' format

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
    
    def getLatestTLE(self, norad_id):
        """
        Obtain latest TLE for a NORAD object
        """
        return self.client.tle_latest(norad_cat_id=norad_id,
                                      iter_lines=True,
                                      ordinal=1,
                                      format=LE_FORMAT)
    
    def getLatestCatalog(self, out_dir=None):
        """
        Obtain catalog of latest TLEs from Space-Track
        """
        return self.client.tle_latest(iter_lines=True, 
                                      epoch='>now-30', 
                                      ordinal=1, 
                                      format=LE_FORMAT)
    
    def getPastTLE(self, norad, start, end, epoch=None):
        """
        Obtain list of TLEs for a NORAD object within an epoch range,
        narrowed down to one (most recent) if desired epoch given
        """
        
        return
    
    def getRunCatGEO(self, start, end, out_dir=None):
        """
        Obtain catalog of GEO TLEs for a given epoch range
        
        Parameters
        ----------
        start, end : str
            Start and end epochs for search, format 'yyyy-mm-dd'
        out_dir : str, optional
            Output directory in which to store catalogue
            Default = None
        
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
                                 format=LE_FORMAT)
        tles = [line for line in result]
        
        print('Number of tles returned: {}'.format(str(len(tles))))
        
        if out_dir is not None:
            with open(out_dir + 'run_cat.txt', 'w') as f:
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
            self.name = name[2:]
        
        self.obs = TOPOS_LOCATION
        self.obj = EarthSatellite(line1, line2, name)
        self.ts = TS
        
        self.norad_id = int(self.line1[2:7])
        self.yearday = float(self.line1[20:32])
        
        self.inclination = float(self.line2[8:16])
        self.eccentricity = float(self.line2[26:33])
        self.raan = float(self.line2[17:25])
        self.argperigree = float(self.line2[34:42])
        self.mean_anomaly = float(self.line2[43:51])
        self.mean_motion = float(self.line2[52:63])
    
    def radec(self, epoch):
        """
        Determine radec coords for a given epoch
        """
        ra, dec, _ = (self.obj - self.obs).at(self.ts.utc(time)).radec()
        return ra._degrees * u.degree, dec.degrees * u.degree  
