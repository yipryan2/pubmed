#!/usr/bin/env python3

import random
import sys

from collections import defaultdict
from itertools import chain, permutations

relationships_dict = {}
# 1 — left gene is human, right gene is mouse
relationships_dict[('9606','10090')] = 1
# 2 — left gene is human, right gene is fish
relationships_dict[('9606','7955')] = 2
# 3 — left gene is human, right gene is fly
relationships_dict[('9606','7227')] = 3
# 4 — left gene is mouse, right gene is human
relationships_dict[('10090','9606')] = 4
# 5 — left gene is mouse, right gene is fish
relationships_dict[('10090','7955')] = 5
# 6 — left gene is mouse, right gene is fly
relationships_dict[('10090','7227')] = 6
# 7 — left gene is fish, right gene is human
relationships_dict[('7955','9606')] = 7
# 8 — left gene is fish, right gene is mouse
relationships_dict[('7955','10090')] = 8
# 9 — left gene is fish, right gene is fly
relationships_dict[('7955','7227')] = 9
# 10 — left gene is fly, right gene is human
relationships_dict[('7227','9606')] = 10
# 11 — left gene is fly, right gene is mouse
relationships_dict[('7227','10090')] = 11
# 12 — left gene is fly, right gene is fish
relationships_dict[('7227','7955')] = 12
# 13 — left gene is hunman, right gene is human
relationships_dict[('9606','9606')] = 13
# 14 — left gene is mouse, right gene is mouse
relationships_dict[('10090','10090')] = 14
# 15 — left gene is fish, right gene is fish
relationships_dict[('7955','7955')] = 15
# 16 — left gene is fly, right gene is fly
relationships_dict[('7227','7227')] = 16

def generate_relationships(data):
    result = {} 
    for groupid, genes in data.items():
        if len(genes) > 1:
            l = []
            for g1, g2 in permutations(genes, 2):
                l.append( (g1[1], relationships_dict[(g1[0], g2[0])], g2[1]) )
            result[groupid] = l
    return result

if __name__ == "__main__":
    homologs = defaultdict(set)

    keep = frozenset(["9606", "10090", "7955", "7227"])

    with open(sys.argv[1]) as f:
        for line in f:
            groupid, species, gene, _, _, _ = line.split("\t")
            if species in keep: 
                homologs[groupid].add( (species, gene) )

    results = list(chain.from_iterable(generate_relationships(homologs).values()))
    random.shuffle(results)

    count = 50000
    fname = 'test'
    f = open(fname, 'w')
    fname = 'valid'
    for r in results:
        f.write("%s\t%s\t%s\n" % r)
        count -= 1
        if fname != 'train' and count == 0:
            f.close()
            f = open(fname, 'w')
            fname = 'train'
        elif count == 0:
            f.close()
            f = open(fname, 'w')
    f.close()
