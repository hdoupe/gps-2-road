import fiona
import shapely
import pickle
import numpy as np
from fips import getFIPS
from util import overlap, pointInBox
from boundedBoxes import getBoundedBoxes
from roads import getRoadsNBoundedBox, unionRoads
import matplotlib.pyplot as plt

from geopy.distance import vincenty

plt.style.use('ggplot')

class Project():
	def __init__(self, routes = None):
		if routes: 	self.routes = routes
		else:
			with open('activity_data/parsed_type_Ride.p', 'rb') as pick: 
				self.routes = pickle.load(pick)

		self.boundedBoxes, self.boxToRoads, self.boxToRoutes = getBoundedBoxes(self.routes)
			

	""" 
		https://www2.usgs.gov/faq/categories/9794/3022
		http://www.latlong.net/degrees-minutes-seconds-to-decimal-degrees
		
		one minute ~ .9 miles
		^ Deg. Decimal = d + (min/60) + (sec/3600)
		==> increase bound by 1/60
	"""
	
	def project(self, boundedBox, inc = 1/60.0, interval = 10):
# 		get relevant roads and routes
		roads, routes = self.boxToRoads[tuple(boundedBox)], self.boxToRoutes[tuple(boundedBox)]
		
		recs = {}
		boxes = []
		
# 		map expanded bounded box to the record and create shapely object for each record
		with fiona.open(roads) as shp:
			for rec in shp:
				rec['object'] = shapely.geometry.shape(rec['geometry'])
				box = rec['object'].bounds
				box = (box[0] - inc, box[1] - inc, box[2] + inc, box[3] + inc)
				recs[box] = rec
				boxes.append(box)
		
		boxes = np.array(boxes)
		roadName = None
		for route in iter(routes):
			try:
				with open('results/' + route['path'] + '_proj.csv', 'w') as results:
					results.write('longitude,latitude,roadname,distance\n')
					geom = route['coordinates']
					d = []
					for i in np.arange(0,geom.shape[0],interval):
						point = shapely.geometry.Point((geom[i,0], geom[i,1]))
						
# 						get all roads with the point in each respective road's bounding box
						candidates = boxes[pointInBox((point.x, point.y), boxes)]
					
						min = (float(1000000),None)
						for j in range(candidates.shape[0]):
							rec = recs[tuple(candidates[j])]
							proj = rec['object'].project(point)
							rpt = rec['object'].interpolate(proj)
							dist = vincenty((point.x, point.y), (rpt.x, rpt.y)).km
							if dist < min[0]: min = (dist,j)
					
						roadName = recs[tuple(candidates[min[1]])]['properties']['FULLNAME']
						results.write(','.join([str(point.x),str(point.y),roadName if roadName else '',str(min[0]),'\n']))		
			
# 			still working out some bugs
			except Exception as e:
				print (e)
				print (route['path'])
				print ('shape',geom.shape)
				print (min)
				print ([str(point.x),str(point.y),roadName if roadName else '',str(min[0]),'\n'])
	
