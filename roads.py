from urllib import request
import zipfile
from io import BytesIO
import os
import time
import fiona
import shapely
import numpy as np
import pickle

from shapely.geometry import shape
from util import overlap
from fips import getFIPS


def getRoads(states = [], counties = []):	
	fips = getFIPS(filter = {'state_abbreviation':states, 'county_name':counties})
	ftp = "ftp://ftp2.census.gov/geo/tiger/TIGER2016/ROADS/tl_2016_{state_fips}{county_fips}_roads.zip"
	dir = 'roads/tiger/{state_fips}{county_fips}_roads'
	
	errors = {'states':[],'counties': []}
	
	for i,row in fips.iterrows():
		state_fips,county_fips = row['state_fips'],row['county_fips']
		print (state_fips,county_fips)
		
		try:
			if os.path.exists(dir.format(state_fips = state_fips, county_fips = county_fips)): continue
		
			rsp = request.urlopen(ftp.format(state_fips = state_fips, county_fips = county_fips), timeout = 10)
			zip = zipfile.ZipFile(BytesIO(rsp.read()))		
			os.mkdir(dir.format(state_fips = state_fips, county_fips = county_fips))
			zip.extractall(dir.format(state_fips = state_fips, county_fips = county_fips))
		
		except Exception as e:
			print (e,state_fips,county_fips)
			errors['states'].append(row['state_abbreviation'])
			errors['counties'].append(row['county_name'])
		
		time.sleep(5)
	
	if len(errors['states']) > 0: 
		time.sleep(300)
		roads(states = errors['states'], counties = errors['counties'])
	
	
def unionRoads(filter = {}):

	base = 'roads/tiger/{state_fips}{county_fips}_roads/tl_2016_{state_fips}{county_fips}_roads.shp'
	
	isAllOpen = False
	allBase = ''
	for var in ['state_fips', 'state_abbreviation', 'county_fips', 'county_name']:
		if var in filter:
			allBase += var + '_' + '_'.join(['_'.join(filter[var])])
	
	allPath = 'test_roads/' + allBase + '/' + allBase + '.shp'
	
	if not os.path.exists('test_roads/' + allBase):
		os.mkdir('test_roads/' + allBase)
	
	fips = getFIPS(filter = filter)

	for i,row in fips.iterrows():
		state_fips,county_fips = row['state_fips'],row['county_fips']
# 		print (state_fips,county_fips)
		
		with fiona.open(base.format(state_fips = state_fips,county_fips = county_fips),'r') as shp:
			
			if not isAllOpen:
				with fiona.open(allPath,'w',driver = shp.driver, crs = shp.crs, schema = shp.schema) as concat:
					for rec in shp:
						concat.write(rec)
				isAllOpen = True
			else:
				with fiona.open(allPath,'a') as concat:
					for rec in shp:
						concat.write(rec)
	
	return allPath
	
def createBoundedBox():
	roadPaths = os.listdir('roads/tiger')
	
	map = {}
	def unpack(l):
		r = [[],[]]
		for t in l: r[0].append(t[0]); r[1].append(t[1])
		return r
		
	for rp in roadPaths:
# 		print (rp)
		coord = [[],[]]
		with fiona.open('roads/tiger/' + rp + '/' + 'tl_2016_' + rp + '.shp', 'r') as shp:
			
			for rec in shp:
				item = rec['geometry']['coordinates']
				if rec['geometry']['type'] == 'LineString': t = [item]
				
				for c in t:
					c = unpack(c)
				
					coord[0] += c[0]
					coord[1] += c[1]

		map[(min(coord[0]),min(coord[1]),max(coord[0]), max(coord[1]))] = {'state_fips':rp[0:2],'county_fips':rp[2:5]}

	return map

def getRoadsNBoundedBox(box):
	with open('roads/roads_bounded_box.p', 'rb') as bb:
		map = pickle.load(bb)
	
	roadBox = np.array(list(map.keys()))
	
	overlapIndex = overlap(box, roadBox)
	overlapped = roadBox[overlapIndex]
	
	results = []
	for i in range(overlapped.shape[0]):
		t = tuple(overlapped[i])
		results.append( map[t] )

	return results


if __name__ == '__main__':
# 	getRoads()
# 	unionRoads()
# 	unionRoads(filter = {'state_abbreviation' : ['GA'], 'county_name':['McDuffie County','Warren County','Glascock County']})

	map = createBoundedBox()
	with open('roads/roads_bounded_box.p', 'wb') as bb:
		pickle.dump(map,bb)
		
	
# 	with open('activity_data/parsed_type_Ride.p', 'rb') as pick: rides = pickle.load(pick)
# 	
# 	c = np.array(rides[0]['coordinates'])

# 	print (c.shape)
# 	
# 	print (c)
# 	print (getRoadsNBoundedBox((np.min(c[:,0]), np.min(c[:,1]), np.max(c[:,0]), np.max(c[:,1]))))
	
	