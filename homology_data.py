#!/usr/bin/env python3

import sys 

from collections import defaultdict
from itertools import combinations

def generate_relationships(data):
    result = {} 
    for groupid, genes in data.items():
        if len(genes) > 1: 
            result[groupid] = combinations(genes, 2)
    return result

if __name__ == "__main__":
    homologs = defaultdict(set)

    keep = frozenset(["9606", "10090", "7955", "7227"])

    with open(sys.argv[1]) as f:
        for line in f:
            groupid, species, gene, _, _, _ = line.split("\t")
            if species in keep: 
                homologs[groupid].add(gene)

    for groupid, genes in generate_relationships(homologs).items():
        print("GroupID: %s" % groupid)
        for gene_1, gene_2 in genes:
            print(" %s - %s" % (gene_1, gene_2))
