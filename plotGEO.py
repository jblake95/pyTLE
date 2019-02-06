"""
Testing platform for GEOPlot software
"""

from tle import (
    parsePlotGEOInput,
    requestFOV,
    TLE,
    Instrument,
    )
import json
import argparse as ap
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import (
    Longitude, 
    Latitude, 
    EarthLocation
    )
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
	
	if args.fov:
		ra_fov, dec_fov = requestFOV()
		instrument = Instrument(args.fov)
	
	for i in range(args.n_steps):
		
		time = start_utc + i*timedelta(minutes=args.timestep)
		print(str(time))
		lst = Time(time, scale='utc', 
		           location=SITE_LOCATION).sidereal_time('apparent')
		
		ha_list = []
		dec_list = []
		for n, norad_id in enumerate(cat):
			
			print('Processing {} {}/{}'.format(str(i+1),
			                                   str(n+1),
                                               str(len(cat))), end="\r")
			
			tle = TLE(cat[norad_id][0], cat[norad_id][1])
			ra, dec = tle.radec(time)
			
			ha_list.append((lst - ra).wrap_at(12*u.hourangle).hourangle)
			dec_list.append(dec)
		
		#plt.style.use('dark_background')
		fig = plt.figure(figsize=(10, 6))
		ax = fig.add_subplot(111)
		
		plt.plot(ha_list, dec_list, 'c.', ms=3)
		
		# Add FOV if requested
		if args.fov:
			ha_fov = Longitude((lst - ra).wrap_at(12*u.hourangle),
			                   u.hourangle)
			
			x = ha_fov - instrument.fov_ra / 2
			y = dec_fov - instrument.fov_dec / 2
			
			fov = Rectangle(xy=(x.hourangle, y.deg),
						    width=instrument.fov_ra.hourangle,
						    height=instrument.fov_dec.deg)
			
			fov.set_facecolor('red')
			fov.set_edgecolor('red')
			print('got here')
			ax.add_artist(fov)
		
		plt.title(str(time))
		
		plt.xlabel('Hour angle / hr')
		plt.ylabel('Declination / $^\circ$')
		
		plt.xlim(-12, 12)
		plt.ylim(-33, 33)
		
		plt.show()
		
		input('enter')
		
		plt.savefig(args.out_dir + 'blah')
