import os
# import matplotlib.pyplot as plt
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
	
""" parse routes to list of line strings """
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
			
		routes.append({'path':routePath,'coordinates':np.array([lons,lats]).T, 'elvations':np.array(elevs),'timestamps':times})
	
	return routes
	
# def allCoordinates(routes):
# 	
# 	with open ('coordinates.csv','w') as c:
# 		mlstr = []
# 		for route in routes:
# 

	
if __name__ == '__main__':
	type = 'Ride'
	rides = getActivityPaths(type = type)
	routes = parseRoutes(rides)
	
	with open('activity_data/parsed_type_' + type + '.p','wb') as handle:
		pickle.dump(routes,handle)
	
# 	routesToShp(routes)
	
# 	with open('activity_data/bike_rides.json','w') as js:
# 		js.write(json.dumps(routes))
	