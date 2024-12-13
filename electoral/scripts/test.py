import src.models.precinct as precinct
import src.models.election as el
from argparse import ArgumentParser
import geojson
import pandas

def decode_geojson_file(filename):
    with open(filename) as file:
        geojson_file = geojson.load(file)
        return geojson_file

def main(args):
    data = pandas.read_csv(args.results, skiprows=args.skip_lines)
    precincts = decode_geojson_file(args.precincts)
    all_precincts = precinct.Precinct.precincts_from_geojson(precincts)
    votes = {}

    for i,row in data[data.TYPE == 'TOTAL'].iterrows():
        votes[row.PRECINCT] = row
    precs_to_write = []
    election = el.Election(2022, {"county": "037"}, all_precincts)
     
    for i,row in data[data.TYPE == 'TOTAL'].iterrows():
        try:
            prec = election.get_precinct(row['PRECINCT'])
            prec.add_results(dict(row))
            precs_to_write.append(prec)
        except KeyError:
            pass

    to_write = precincts.copy()
    to_write['features'] = [p.as_dict() for p in precs_to_write]
    fname = f"{args.output_filename}"
    if not fname.startswith("maps"):
        fname = f"maps/{fname}"
    if not fname.endswith("geojson"):
        fname = f"{fname}.geojson"
    if args.name:
        to_write['name'] = args.name
    with open(fname, "w") as f:
        f.write(geojson.dumps(to_write))


if __name__ == "__main__":
    argument_parser = ArgumentParser()
    argument_parser.add_argument("precincts", help="geojson for precincts")
    argument_parser.add_argument("results", help="single-race precinct-level results to convert")
    argument_parser.add_argument("output_filename", help="filename to output results as geojson")
    argument_parser.add_argument("-s", "--skip-lines", type=int, help="number of lines to skip in csv results")
    argument_parser.add_argument("-n", "--name", help="name for layer")
    args = argument_parser.parse_args()
    main(args)
