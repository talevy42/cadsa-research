import geojson
import re


class Precinct:

    election: str
    id: str
    geometry: object
    metadata: object
    results: object

    def __init__(self, election, pid, geometry=None, metadata={}, results={}) -> None:
        self.election = election
        self.id = pid
        matched = re.match('(\d+)(.+)', pid)
        self.number = matched.group(1)
        self.geometry = geometry
        self.metadata = metadata
        self.results = results
        self.precinct_meta = {}

    def add_results(self, results) -> None:
        self.results = results

    def add_geometry(self, geometry) -> None:
        self.geometry = geometry

    def add_meta(self, metadata) -> None:
        self.metadata = metadata

    @classmethod
    def precincts_from_geojson(cls, data, file=False):
        precincts = []
        if file:
            data = geojson.load(open(data))
        for pr in data['features']:
            if pr["geometry"]["type"] == "GeometryCollection":
                geometry = geojson.MultiPolygon(pr["geometry"]["geometries"])
            elif pr["geometry"]["type"] == "MultiPolygon":
                geometry = geojson.MultiPolygon(pr["geometry"])
            else:
                geometry = geojson.Polygon(pr["geometry"])
            props = pr['properties']
            pid = props['PRECINCT']
            # c1 = props['CTRACT1']
            # c2 = props['CTRACT2']
            if props.get("TYPE", "TOTAL") == "TOTAL":
                precincts.append(cls("2022p", pid, geometry, props))
        return precincts

    def add_data(self, label, data, datatype=None):
        if datatype is not None:
            self.metadata[datatype][label] = data
        else:
            self.metadata[label] = data

    def as_dict(self):
        props = self.metadata.copy()
        props['id'] = self.id
        props['number'] = self.number
        props.update(self.results)
        return {"type": "Feature", "geometry": self.geometry, "properties": props}
