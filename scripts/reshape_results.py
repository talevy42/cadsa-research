import csv
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


def main(args):
    prec_id_col = args.precinct_column

    rf = open(args.results_file, "r")
    next(rf)
    next(rf)
    results = csv.DictReader(rf)

    mappings = csv.DictReader(open(args.districts_map, newline=""))

    precinct_map = {}
    for m in mappings:
        code = m["Code"]
        if code in precinct_map:
            if m["percent"] > precinct_map[code]["percent"]:
                precinct_map[code] = m
        else:
            precinct_map[code] = m

    reshaped = {}
    for precinct in results:
        if precinct.get("TYPE", "TOTAL") != "TOTAL" or precinct[prec_id_col] not in precinct_map:
            pass
        else:
            district = precinct_map[precinct[prec_id_col]]["District"]
            if district not in reshaped:
                new_results_block = {k: 0 for k in args.results_cols}
                new_results_block["district"] = district
                new_results_block[args.total] = 0
                reshaped[district] = new_results_block
            for k in args.results_cols:
                reshaped[district][k] += int(precinct[k])
            reshaped[district][args.total] += int(precinct[args.total])

    writer = csv.DictWriter(
        open(args.outfile, "w", newline=""), ["district", args.total] + args.results_cols
    )
    writer.writeheader()
    for _, results in reshaped.items():
        writer.writerow(results)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Translator for taking precinct-level results and reshaping to new districts",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("results_file", type=str, help="CSV filename for precinct-level results")
    parser.add_argument(
        "districts_map", type=str, help="CSV filename mapping precincts to districts"
    )
    parser.add_argument(
        "-o", "--outfile", type=str, help="CSV filename to write out results", default="out.csv"
    )
    parser.add_argument(
        "-pc", "--precinct_column", type=str, default="PRECINCT", help="Column name for precinct id"
    )
    parser.add_argument(
        "-t", "--total", type=str, default="BALLOTS CAST", help="Column name for total votes"
    )
    parser.add_argument(
        "-rc",
        "--results_cols",
        nargs="+",
        help="<Required> List columns to sum from the results file",
    )

    args = parser.parse_args()
    main(args)
