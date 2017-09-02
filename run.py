from roads import *
from routes import *
from project import Project


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


if __name__ == '__main__':
	main(states=['GA', 'DC'])
