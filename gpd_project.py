import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.strtree import STRtree
from shapely.geometry import MultiLineString
from geopy.distance import vincenty


class Project():
    def __init__(self, roads):
        self.roads = roads
        ml = MultiLineString(list(self.roads.geometry))
        self.rtree = STRtree(ml)

    def project_point(self, point):
        results = self.rtree.query(point)
        minimizer = (1000000.0, None)
        for result in results:
            proj = result.project(point)
            rpt = result.interpolate(proj)
            dist = vincenty((point.x, point.y), (rpt.x, rpt.y)).km
            if dist < minimizer[0]:
                minimizer = (dist, result)

        # way to slow
        # return self.roads.loc[self.roads.geometry==minimizer[1],]

        return minimizer[1]


def map_match(route, roads):
    project = Project(roads)
    # project = lambda pt: project.project_point(pt)
    results = route.geometry.apply(project.project_point)

if __name__ == "__main__":
    route_path = "/Users/HANK/Documents/activities/gps_2_road/activity_data/Point_shp_data/20170827-121415-Ride"
    route = gpd.read_file(route_path)
    road_path = "/Users/HANK/Documents/activities/gps_2_road/roads/tiger/11001_roads"
    roads = gpd.read_file(road_path)
    map_match(route, roads)
