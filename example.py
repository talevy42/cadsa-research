import geojson
import models.precinct as prec
import models.election as el

def decode_geojson_file(filename):
    with open(filename) as file:
        geojson_file = geojson.load(file)
        return geojson_file

def main():
    precincts = decode_geojson_file("maps/precincts_2022.geojson")
    meta = precincts.copy()
    del meta['features']
    precinct_meta = meta
	all_precincts = prec.Precinct.precincts_from_geojson(precincts)
	election = el.Election(2022, {"county": "037"}, all_precincts)
	fields = {"income": "B06011_001E" }
	election.add_census_data(fields)

if __name__ == "__main__":
    main()
