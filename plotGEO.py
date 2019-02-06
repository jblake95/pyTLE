"""
Testing platform for GEOPlot software
"""

from tle import (
    parsePlotGEOInput,
    TLE,
    Instrument,
    )
import json
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import (
    Longitude, 
    Latitude, 
    EarthLocation
    )
from datetime import timedelta
import matplotlib.pyplot as plt

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

SITE_LATITUDE = 28.7603135
SITE_LONGITUDE = -17.8796168
SITE_ELEVATION = 2387

SITE_LOCATION = EarthLocation(lat=SITE_LATITUDE*u.deg,
                              lon=SITE_LONGITUDE*u.deg,
                              height=SITE_ELEVATION*u.m)

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
    
    parser.add_argument('cat_path',
                        help='path to catalogue json file',
                        type=str)
    
    parser.add_argument('out_dir',
                        help='output directory for resulting plots',
                        type=str)
    
    parser.add_argument('start',
                        help='start of night [utc], '
                             'format "YYYY-mm=ddTHH:MM:SS"',
                        type=str)
    
    parser.add_argument('timestep',
                        help='timestep between each plot [minutes]',
                        type=int)
    
    parser.add_argument('n_steps',
                        help='number of timesteps',
                        type=int)
    
    parser.add_argument('--fov',
                        help='plot field of view? Specify instrument: \n'
                             'INT, SuperWASP, RASA',
                        type=str)
    
    parser.add_argument('--zoom',
                        help='zoom into field of view?',
                        action='store_true')
    
    return parser.parse_args()

if __name__ == "__main__":
	
	args = argParse()
	
	try:
		with open(args.cat_path, 'r') as cp:
			cat = json.load(cp)
	except FileNotFoundError:
		print('No catalogue file found. Please rectify...')
		quit()
	
	start_utc = parsePlotGEOInput(args)
	
	"""
	if args.fov:
		instrument = Instrument(args.fov)
	"""
	
	for i in range(args.n_steps):
		
		print('Processing {}/{}'.format(str(i),
                                        str(args.n_steps)), end="\r")
		
		time = start_utc + i*timedelta(minutes=args.timestep)
		lst = Time(time, scale='utc', 
		           location=SITE_LOCATION).sidereal_time('apparent')
		
		ha_list = []
		dec_list = []
		for n, norad_id in enumerate(cat):
			
			print('TLE {}/{}'.format(str(n),
                                     str(len(cat))), end="\r")
			
			tle = TLE(cat[norad_id][0], cat[norad_id][1])
			ra, dec = tle.radec(time)
			
			ha_list.append((lst - ra).wrap_at(12*u.hourangle).hourangle)
			dec_list.append(dec)
		
		plt.figure(figsize=(10, 4))
		plt.style.use('dark_background')
		
		plt.plot(ha_list, dec_list, color=plt.cm.cool(0.28), s=2)
		
		plt.title(str(time))
		
		plt.xlabel('Hour angle / hr')
		plt.ylabel('Declination / $^\circ$')
		
		plt.show()
		
		input('enter')
		
		plt.savefig(args.out_dir + )
