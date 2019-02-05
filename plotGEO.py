"""
Testing platform for GEOPlot software
"""

from tle import (
    TLE,
    Instrument,
    )
import json
from datetime import timedelta

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
	
	if args.fov:
		instrument = Instrument(args.fov)
	
	
