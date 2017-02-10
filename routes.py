import os
import numpy as np
import fiona
from bs4 import BeautifulSoup
import json
import pickle

from shapely.geometry import Point


def getActivityPaths(type = 'Ride'):
	activities = os.listdir('activity_data/gpx_data')
	rides = []
	for a in activities:
		if type in a: rides.append(a)
	
	return rides
	
""" parse routes in gpx file to dictionary containing:
		path: source gpx file
		coordinates: list of (longitude, latitude)
		elevations: list of elevation above sea level in meters
		timestamp: time of gps emission
"""
def parseRoutes(routePaths):
	routes = []
	for routePath in routePaths:
		with open('activity_data/gpx_data/' + routePath) as f:
			soup = BeautifulSoup(f.read(),'lxml')
	
		lons, lats, elevs, times = [],[],[],[]
		
		metadata = soup.find('metadata')
		date = metadata.find('time')
		date = date.get_text()
				
		for trkpt in soup.find_all('trkpt'):
			lons.append(float(trkpt['lon']))
			lats.append(float(trkpt['lat']))
								
			elev = trkpt.find('ele')
			elev = float(elev.get_text())
			elevs.append(elev)
					
			time = trkpt.find('time')		
			times.append(time.get_text())
			
		routes.append({'path':routePath,'coordinates':np.array([lons,lats]).T, \
			'elvations':np.array(elevs),'timestamps':times})
	
	return routes
