#!/usr/bin/env python3

import argparse
import csv
import gzip
import json
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("gzfile", help="gziped csv input file")
parser.add_argument("-o", "--output", help="write json output to file")
 
args = parser.parse_args()
 
if not args.output:
    args.output = Path(args.gzfile).stem + '.json'

print("Writing json output to %s" % args.output)

cols_map = { 'GeneID' : 'NCBI gene ID',
             'Symbol' : 'Symbol',
             'Full_name_from_nomenclature_authority' : 'Full name',
             'Synonyms' : 'Synonyms',
             'Organism' : 'Organism',
             'Modification_date' : 'Updated' }

json_data = []

with gzip.open(args.gzfile, mode='rt') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t')
    for row in csv_reader:
        row['GeneID'] = int(row['GeneID'])
        json_data.append({v:row[k] if k != 'Organism' else 0 for k,v in cols_map.items()})

print("No. of RefSeq IDs: %d" % len(json_data))

with open(args.output, 'w') as json_out_file:
    json.dump(json_data, json_out_file, indent=4, sort_keys=False)
