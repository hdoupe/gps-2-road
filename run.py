from roads import *
from routes import *
from project import Project

import geopandas as gpd
import fips

def main(states=[]):
	print ('getting roads...')
	getRoads(states=states)
	print ('creating inverse map of road to bounded box...')
	road_map = get_road_map()
	print ('parsing activities...')
	activity_type = 'Ride'
	paths = getActivityPaths(activity_type = activity_type)
	routes = parseRoutes(paths)
	print ('projecting activities...')
	proj = Project(routes)

	for i in range(proj.boundedBoxes.shape[0]):
		print(i/float(proj.boundedBoxes.shape[0]))
		proj.project(proj.boundedBoxes[i], interval = 10)


def main2():
	route_path = "/Users/HANK/Documents/activities/gps_2_road/activity_data/Point_shp_data/20170827-121415-Ride"
	route = gpd.read_file(route_path)
	fips_df = fips.get_overlapping_counties(route)
	getRoads(fips_df=fips_df)

if __name__ == '__main__':
	main2()
	# main(states=['GA', 'DC'])
