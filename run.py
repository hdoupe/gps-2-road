from roads import *
from routes import *
from project import Project


def main(states = ['GA']):
	print ('getting roads...')
	getRoads(states = states)
	print ('creating map...')
	map = createBoundedBox()
	
	print ('parsing activities...')
	type = 'Ride'
	rides = getActivityPaths(type = type)
	routes = parseRoutes(rides)
	
	print ('projecting activities...')
	proj = Project(routes)
	
	for i in range(proj.boundedBoxes.shape[0]):
		proj.project(proj.boundedBoxes[i], interval = 10)


if __name__ == '__main__':
	main()