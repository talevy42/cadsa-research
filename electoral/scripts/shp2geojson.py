import geopandas as gpd
import sys

def convert(filename, outname):
    df = gpd.read_file(filename)
    df.to_file(outname, driver='GeoJSON')

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
