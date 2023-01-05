import sys
import geopandas as gpd
import csv

EXPORT_COLS = ["District", "area_col", "Code", "percent"]


def convert(precinct_file, district_file, output_file):
    precincts = gpd.read_file(precinct_file).to_crs("EPSG:4326")
    districts = gpd.read_file(district_file).to_crs("EPSG:4326")
    overlay = districts.overlay(precincts, how="intersection")
    overlay["area_col"] = overlay.area
    overlay["percent"] = overlay.apply(
        lambda x: x.area_col / precincts[precincts.Code == x.Code].area.sum(), axis=1
    )
    overlay[overlay.percent > 0.1][EXPORT_COLS].to_csv(output_file)


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
