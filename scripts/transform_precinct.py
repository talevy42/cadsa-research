import sys
import geopandas as gpd
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import csv

EXPORT_COLS = ["District", "area_col", "percent", "precinct"]


def convert(args):
    precincts = gpd.read_file(args.precinct_file).to_crs("EPSG:4326")
    districts = gpd.read_file(args.district_file).to_crs("EPSG:4326")
    code_col = args.code_col
    overlay = districts.overlay(precincts, how="intersection")
    overlay["area_col"] = overlay.area
    try:
        overlay["percent"] = overlay.apply(
            lambda x: x.area_col / precincts[precincts[code_col] == x[code_col]].area.sum(), axis=1
        )
        overlay.rename(columns={code_col: "precinct"}, inplace=True)
        overlay[overlay.percent > 0.1][EXPORT_COLS].to_csv(args.output_file)
    except (AttributeError, KeyError) as e:
        print(f"Valid cols: {list(precincts.columns)}")
        raise e


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Translator for taking precinct shapefiles and generating "
        + "a mapping to new districts",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("precinct_file", type=str, help="Shapefile for precincts")
    parser.add_argument("district_file", type=str, help="Shapefile for new districts")
    parser.add_argument(
        "output_file", default="out.csv", type=str, help="CSV filename for mappings"
    )
    parser.add_argument(
        "-c", "--code-col", type=str, default="Code", help="Column name for precinct id"
    )
    args = parser.parse_args()
    convert(args)
