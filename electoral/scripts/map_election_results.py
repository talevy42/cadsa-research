import pandas as pd
import geojson
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import electoral.models.precinct as prec
import electoral.models.election as el


def decode_geojson_file(filename):
    with open(filename) as file:
        geojson_file = geojson.load(file)
        return geojson_file


def main(args):
    results_data = pd.read_csv(args.results_file, skiprows=args.num_skip)

    precincts = decode_geojson_file(args.precincts_file)
    precinct_meta = precincts.copy()
    del precinct_meta["features"]
    print(len(results_data))

    all_precincts = prec.Precinct.precincts_from_geojson(precincts)
    election = el.Election(2024, {"county": "037"}, all_precincts)
    votes = {}

    for i, row in results_data[results_data.TYPE == "TOTAL"].iterrows():
        votes[row.PRECINCT] = row
    precs_to_write = []
    for i, row in results_data[results_data.TYPE == "TOTAL"].iterrows():
        try:
            precinct = election.get_precinct(row["PRECINCT"])
            row_save = dict(row)
        except KeyError:
            continue
        for r in args.results_rows:
            if row[args.total] == 0:
                print(row)
            row_save[f"Percent {r}"] = 100 * row[r] / max(row[args.total], 1)
        if args.registration:
            row_save["Turnout"] = 100 * row[args.total] / int(row[args.registration])
        precinct.add_results(row_save)
        precs_to_write.append(precinct)

    with open(args.outfile, "w") as f:
        to_write = precinct_meta.copy()
        to_write["features"] = [p.as_dict() for p in precs_to_write]
        f.write(geojson.dumps(to_write))


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Translator for taking precinct shapefiles and augmenting them with results",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("results_file", type=str, help="CSV filename for precinct-level results")
    parser.add_argument("precincts_file", type=str, help="Geojson file name for precinct shapefile")
    parser.add_argument(
        "-o",
        "--outfile",
        default="out.geojson",
        type=str,
        help="Geojson filename to write out results",
    )
    parser.add_argument(
        "-pc", "--precinct_column", type=str, default="PRECINCT", help="Column name for precinct id"
    )
    parser.add_argument(
        "-t", "--total", type=str, default="BALLOTS CAST", help="Column name for total votes"
    )
    parser.add_argument(
        "-n", "--num_skip", type=int, default=0, help="Number of header lines to skip in results"
    )
    parser.add_argument("-r", "--results_rows", type=str, nargs="+", default=[])
    parser.add_argument("--registration", type=str)
    args = parser.parse_args()
    main(args)
