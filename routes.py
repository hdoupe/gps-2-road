import os
import numpy as np
import fiona
from bs4 import BeautifulSoup
import json

from shapely.geometry import Point


def getActivityPaths(activity_type = 'Ride'):
	activities = os.listdir('activity_data/gpx_data')
	paths = []

	for a in activities:
		if activity_type in a:
			paths.append(a)

	return paths

""" parse routes in gpx file to dictionary containing:
		path: source gpx file
		coordinates: list of (longitude, latitude)
		elevation: list of elevation above sea level in meters
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
			'elvation':np.array(elevs),'timestamp':times})

	return routes


def routes_to_shp(routes):
	def format_coordinates(coordinates):
		formatted = []
		for i in range(coordinates.shape[0]):
			formatted.append((coordinates[i, 0], coordinates[i, 1]))

		return formatted


	path_out = "routes_shp/routes.shp"
	with fiona.open(path_out, "w",
	                crs={'init': 'epsg:4269'},
					driver="ESRI Shapefile",
					schema={'properties': {'path': 'str:50',
					                       'time': 'str:50'},
					        'geometry': 'LineString'}) as shp:

		for i in range(len(routes)):
			route = routes[i]
			rec = {}
			rec['id'] = str(i)
			rec['geometry'] = {'coordinates': format_coordinates(route['coordinates']),
			                   'type': 'LineString'}
			rec['properties'] = {'path':route['path'],
			                     'time': route['timestamp'][0]}

			shp.write(rec)


def routes_to_shp_setup(activity_type='Ride'):
	paths = getActivityPaths(activity_type = activity_type)
	routes = parseRoutes(paths)
	routes_to_shp(routes)
