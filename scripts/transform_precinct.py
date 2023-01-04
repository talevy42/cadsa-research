import geopandas as gpd
import csv

def convert(precinct_file, district_file, output_file):
    precincts = gpd.read_file(precinct_file)
    districts = gpd.read_file(district_file)

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
