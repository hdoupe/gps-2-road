import os

import routes
import roads
import gpd_project

import geopandas as gpd
import fips

def runner():
    print("converting route gpx files to shp files...")
    routes.convert_all_gpx_to_shp(activity_type='Ride', output_type="Point")
    print("reading route shp files in as dataframes...")
    route_gpds = routes.get_geopandas_from_shp(activity_type="Ride",
	                                            output_type="Point")
    print("projecting routes...")
    for route_gpd in route_gpds:
        print("\troute: ", route_gpd.iloc[0].path)
        print("\tgetting road data...")
        print("\t\toverlapping_counties...")
        fips_df = fips.get_overlapping_counties(route_gpd)
        if len(fips_df) == 0:
            print("\t\tno overlapping counties-->continue")
            continue
        print("\t\tfetch tiger data...")
        roads.getRoads(fips_df=fips_df)
        print("\t\tconcatenate road shp files to geopandas dataframes")
        roads_df = roads.concatenate_roads(fips_df=fips_df)

        print("\tprojecting route...")
        proj = gpd_project.Project(roads_df)
        route_gpd["road_name"] = route_gpd.geometry.apply(proj.project_point)

        print("\twriting results...")
        route_name = route_gpd.iloc[0].path.split('.')[0]
        if not os.path.exists("results/" + route_name):
            os.mkdir("results/" + route_name)
        route_gpd.to_file("results/" + route_name)


if __name__ == '__main__':
	main2()
	# main(states=['GA', 'DC'])
