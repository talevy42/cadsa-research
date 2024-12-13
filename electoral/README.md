# Typical process for Los Angeles

- Find election precincts shapefile [here](https://egis-lacounty.hub.arcgis.com/datasets/5c711a6ba4db46a489963658493c6d5d_0/explore?location=33.797808%2C-118.298780%2C7.71)
- Download statement of votes cast (excel format) [here](https://www.lavote.gov/home/voting-elections/current-elections/election-results/past-election-results)

```
xlstocsv ~/path/to/statementofvote.xls
mv statementofvote.csv data/
python3 scripts/map_election_results.py data/statementofvote.csv path/to/shapefile.geojson -n 2 -r {"CANDIDATE NAMES" ...} -o electionyear_district.geojson
```

- Import the geojson into qgis.
- Style appropriately using the candidate and percent rows
- Use qgis cloud to publish the data and the map