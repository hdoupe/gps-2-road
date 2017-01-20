import numpy as np
from util import overlap
from roads import unionRoads, getRoadsNBoundedBox

def getBoundedBoxes(rides):
	""" 
		iterate over rides find all bounded boxes
		objective: minimize area in bounded boxes subject to all ride data points
		are contained in bounded boxes
		
		create mapping from each bounding box to the roads contained in that box and
		the rides contained in that box
	"""
	boundedBoxes = np.array([[],[],[],[]]).T
	boxToRides = {}
	for ride in iter(rides):
		box = getBoundedBox(ride['coordinates'])
		
		if box in boxToRides: 	boxToRides[box].append(ride)
		else: 					boxToRides[box] = [ride]
		
		if boundedBoxes.shape[0] > 0:
			""" get all already discovered bounded boxes that overlap with ride bb """
			overlappedIndex = overlap(box, boundedBoxes)
			overlapped = boundedBoxes[overlappedIndex]
			""" 
				if overlap then remove overlapped boxes from boundedBoxes, merge 
				over lapped bounded boxes, place new bounded box back in boundedBoxes
			"""
			if overlapped.shape[0] > 0:
				
				boundedBoxes = boundedBoxes[~overlappedIndex]				
				
				overlapped = np.vstack((box,overlapped))
				
				update = []
				for i in range(overlapped.shape[0]): 
					update += boxToRides[tuple(overlapped[i])]
					boxToRides.pop(tuple(overlapped[i]), None)
				
				overlapped = mergeBoundedBoxes(overlapped)
				
				boxToRides[overlapped] = update
				
				boundedBoxes = np.vstack((boundedBoxes, overlapped))
			else:
				boundedBoxes = np.vstack((boundedBoxes, box))
		else:
			boundedBoxes = np.vstack((boundedBoxes, box))
	
	boxToRoads = {}
	for i in range(boundedBoxes.shape[0]):
		bb = tuple(boundedBoxes[i])
		fips = getRoadsNBoundedBox(bb)
		filter = {'state_fips':[f['state_fips'] for f in fips], \
			'county_fips':[f['county_fips'] for f in fips]}
		boxToRoads[bb] = unionRoads(filter = filter)

	return boundedBoxes, boxToRoads, boxToRides


def getBoundedBox(coord):
	return (np.min(coord[:,0]), np.min(coord[:,1]), np.max(coord[:,0]), np.max(coord[:,1]))

def mergeBoundedBoxes(boxes):
	return (np.min(boxes[:,0]), np.min(boxes[:,1]), np.max(boxes[:,2]), np.max(boxes[:,3]))

