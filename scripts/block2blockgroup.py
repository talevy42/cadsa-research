import sys
import csv

def convert(filename, outname):
    reader = csv.reader(open(filename, newline=''))
    results = {}
    for line in reader:
        new_id = line[0][:12]
        results[f'"{new_id}"'] = line[1]
    writer = csv.writer(open(outname, "w", newline=''), quotechar = "'")
    for k, v in results.items():
        writer.writerow([k, v])

if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
