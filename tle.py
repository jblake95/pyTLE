"""
Module for dealing with Space-Track elsets
"""

import json
import getpass as gp
from operator import itemgetter
from astropy import units as u
from spacetrack import SpaceTrackClient
import spacetrack.operators as op
from datetime import (
    datetime,
    timedelta,
    )
from skyfield.api import (
    load, 
    Topos, 
    utc,
    )
from skyfield.sgp4lib import EarthSatellite

TS = load.timescale() # save repeated use in iterative loops
LE_FORMAT = '3le'     # TODO: generalise to allow for 'tle' format

SITE_LATITUDE = '28.7603135 N'
SITE_LONGITUDE = '17.8796168 W'
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
            self.e_lim = '<0.01'
            self.mm_lim = '0.99--1.01'
        elif orb_type.lower() in LEO_CHECK:
            self.e_lim = '<0.25'
            self.mm_lim = '>11.25'
        elif orb_type.lower() in MEO_CHECK:
            self.e_lim = '<0.25'
            self.p_lim = '600--800'
        elif orb_type.lower() in HEO_CHECK:
            self.e_lim = '>0.25'
        elif orb_type.lower() in ALL_CHECK:
            print('Full catalogue specified; no limits placed.')
        else:
            print('Incorrect format! Please provide a valid' 
                  'orbit type... \n'
                  'GEO - "g" \n'
                  'LEO - "l" \n'
                  'MEO - "m" \n'
                  'HEO - "h" \n'
                  'ALL - "a" \n')
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
    
    def getRunCat(self, dates, cat_type, out_dir=None):
        """
        Obtain catalog of GEO TLEs for a given epoch range
        
        Parameters
        ----------
        dates : array-like
            List of (start, end) tuples corresponding to appropriate 
            limits for querying the Space-Track API
        cat_type : str
            Type of objects to be queried (e.g. 'geo')
        out_dir : str, optional
            Output directory in which to store catalogue
            Default = None
        
        Returns
        -------
        tles : array-like
            Element sets returned from query to SpaceTrack
        """
        orb = Orbit(cat_type) 
        
        tles = []
        for date in dates:
            date_range = '{}--{}'.format(date[0].strftime('%Y-%m-%d'),
                                         date[1].strftime('%Y-%m-%d'))
            
            if cat_type in GEO_CHECK + LEO_CHECK: 
                result = self.client.tle(iter_lines=True,
                                         eccentricity=orb.e_lim,
                                         mean_motion=orb.mm_lim,
                                         epoch=date_range,
                                         limit=200000,
                                         format=LE_FORMAT)
            elif cat_type in MEO_CHECK:
                result = self.client.tle(iter_lines=True,
                                         eccentricity=orb.e_lim,
                                         period=orb.p_lim,
                                         epoch=date_range,
                                         limit=200000,
                                         format=LE_FORMAT)
            elif cat_type in HEO_CHECK:
                result = self.client.tle(iter_lines=True,
                                         eccentricity=orb.e_lim,
                                         epoch=date_range,
                                         limit=200000,
                                         format=LE_FORMAT)
            elif cat_type in ALL_CHECK:
                result = self.client.tle(iter_lines=True,
                                         epoch=date_range,
                                         limit=200000,
                                         format=LE_FORMAT)
            else:
                print('Incorrect format! Please supply a valid' 
                      'orbit type... \n'
                      'GEO - "g" \n'
                      'LEO - "l" \n'
                      'MEO - "m" \n'
                      'HEO - "h" \n'
                      'ALL - "a" \n')
            tles += [line for line in result]
        
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
        self.yday = float(self.line1[20:32])
        
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
        epoch = epoch.replace(tzinfo=utc)
        ra, dec, _ = (self.obj-self.obs).at(self.ts.utc(epoch)).radec()
        
        return ra.degrees * u.degree, dec.degrees * u.degree

class Instrument:
    """
    Convenience class for instrumental properties
    """
    def __init__(self, instrument):
        if instrument.lower() == 'int':
            self.fov_ra = 0.5
            self.fov_dec = 0.5

def parseRunInput(args):
    """
    Read the run_cat input arguments in a more useful format
    
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
        print('Incorrect format! Please supply dates "YYYY-mm-dd"...')
        quit()
    
    return start_date, end_date

def parseEpochInput(args):
    """
    Read the epoch_cat input arguments in a more useful format
    
    Parameters
    ----------
    args: argparse object
        Arguments returned by argparse user interaction
    
    Returns
    -------
    epoch : datetime object
        Desired epoch in datetime format
    """
    return datetime.strptime(args.epoch, '%Y-%m-%dT%H:%M:%S')

def checkRunLength(start, end, cat_type):
    """
    Check length of run to ensure query does not exceed limit
    
    Parameters
    ----------
    start, end : datetime object
        Start and end epochs for the run (after leniency corrections)
    cat_type : str
        Type of objects to be queried (e.g. 'geo')
    
    Returns
    -------
    dates : array-like
        List of (start, end) tuples corresponding to appropriate 
        limits for querying the Space-Track API
    """
    if cat_type.lower() in GEO_CHECK + MEO_CHECK + HEO_CHECK:
        max_time = 20 
    elif cat_type.lower() in LEO_CHECK + ALL_CHECK:
        max_time = 2 
    else:
        print('Incorrect format! Please supply a valid orbit type... \n'
              'GEO - "g" \n'
              'LEO - "l" \n'
              'MEO - "m" \n'
              'HEO - "h" \n'
              'ALL - "a" \n')
        quit()
    
    run_length = end - start 
    
    dates = []
    if run_length.days > max_time:
        
        rem = run_length.days % max_time
        n_chunks = run_length.days // max_time
        for i in range(n_chunks):
            dates.append((start + timedelta(days=i*max_time),
                          start + timedelta(days=(i+1)*max_time)))
        
        dates.append((start + timedelta(days=n_chunks*max_time),
                      start + timedelta(days=n_chunks*max_time + rem)))
    
    return dates

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

def getFractionalYearDay(epoch):
    """
    Convert a datetime object to day of the year with frational 
    portion of the day
    
    Parameters
    ----------
    epoch : datetime object
        Epoch to convert to year day
    
    Returns
    -------
    yday : float
        Corresponding year day
    """
    frac = epoch.hour / 24. + epoch.minute / 60. + epoch.second / 60.
    
    return epoch.timetuple().tm_yday + frac

def getEpochCat(run_cat, epoch, out_dir=None):
    """
    Obtain appropriate catalogue for a desired epoch
    
    Parameters
    ----------
    run_cat : dict
        Run catalogue, organised by norad id
    epoch : datetime object
        Desired epoch to compare tles against
    out_dir : str, optional
        Output directory in which to store resulting catalogue
        Default = None
    
    Returns
    -------
    epoch_cat : dict
        Catalogue of tles for desired epoch
    """
    epoch_yday = getFractionalYearDay(epoch)
    
    epoch_cat = {}
    for n, norad_id in enumerate(run_cat.keys()):
        print('Processing {}/{}'.format(str(n),
                                        str(len(run_cat.keys()))), end="\r")
        t_diff = []
        for tle in run_cat[norad_id]:
            t = TLE(tle[0], tle[1])
            t_diff.append(abs(epoch_yday - t.yday))
        min_idx = min(enumerate(t_diff), key=itemgetter(1))[0]
        epoch_cat.update({norad_id:run_cat[norad_id][min_idx]})
    
    if out_dir is not None:
        with open(out_dir + 'epoch_cat.json', 'w') as f:
            json.dump(epoch_cat, f)
    
    return epoch_cat
