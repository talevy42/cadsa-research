import us
from census import Census
from typing import Dict
from .precinct import Precinct

C_KEY = "d56aeca639f90ccb4bb9f85af67f0f8402e81c24"


def census_lookup(fields, cen, meta):
    return_dict = {}
    data = cen.acs5.get(list(fields.values()), meta)
    for row in data:
        return_dict[row['tract']] = row
    return return_dict


class Election:

    year: int
    precincts: Dict[str, Precinct]
    metadata: dict
    cache: dict

    def __init__(self, year, metadata={}, precincts={}):
        self.year = year
        self.metadata = metadata
        if isinstance(precincts, list):
            self.precincts = {p.id: p for p in precincts}
        else:
            self.precincts = precincts
        self.cache = {}

    def get_meta(self):
        in_clause = "state:{}".format(us.states.CA.fips)
        if "county" in self.metadata:
            in_clause += "+county:{}".format(self.metadata['county'])
        return {"for": "tract:*", "in": in_clause}

    def add_census_data(self, fields, is_str=False, cen=None):
        if cen is None:
            cen = Census(C_KEY)
        meta = self.get_meta()
        data = census_lookup(fields, cen, meta)
        for _, prec in self.precincts.items():
            pid = prec.metadata['CTRACT2']
            for label, code in fields.items():
                if pid in data:
                    print(data[pid][code])
                    prec.add_data(label, data[pid][code])
                else:
                    prec.add_data(label, "" if is_str else 0)

    def get_precinct(self, pid):
        return self.precincts[pid]

    def get_precincts(self):
        return list(self.precincts.values())
