import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.strtree import STRtree
from shapely.geometry import MultiLineString
from geopy.distance import vincenty


class Project():
    def __init__(self, roads):
        self.roads = roads
        self.rtree = None

    def project_point(self, point, multilinestring):
        minimizer = (1000000.0, None)
        for ml in multilinestring:
            proj = ml.project(point)
            rpt = ml.interpolate(proj)
            dist = vincenty((point.x, point.y), (rpt.x, rpt.y)).km
            if dist < minimizer[0]:
                minimizer = (dist, ml)

        # way to slow
        # return self.roads.loc[self.roads.geometry==minimizer[1],]

        return minimizer[1]


    def set_RTree(self):
        self.ml = MultiLineString(list(self.roads.geometry))
        self.rtree = STRtree(self.ml)


    def project_point_rtree(self, point):
        if self.rtree is None:
            self.set_RTree()
        hits = self.rtree.query(point)
        return self.project_point(point, hits)


    # def set_name_property(self):
    #
    #     def _set_name_prop(row):
    #         setattr(row["geometry"], "FULLNAME", row["FULLNAME"])
    #
    #     self.roads.apply(_set_name_prop, axis=1)


def map_match_rtree(route, roads):
    project = Project(roads)
    # project = lambda pt: project.project_point_rtree(pt)
    results = route.geometry.apply(project.project_point_rtree)
    print (results)

    results.to_file('results0.shp')


if __name__ == "__main__":
    route_path = "/Users/HANK/Documents/activities/gps_2_road/activity_data/Point_shp_data/20170827-121415-Ride"
    route = gpd.read_file(route_path)
    road_path = "/Users/HANK/Documents/activities/gps_2_road/roads/tiger/11001_roads"
    roads = gpd.read_file(road_path)
    map_match_rtree(route, roads)
