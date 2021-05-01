#!/usr/bin/env python3

import eutils

out_filename = 'abstracts.json'
number_of_abstract = 493709
querykey = '1'
webenv = 'MCID_608d9d1a11e72567cd2f1f7a'
print("Number of abstract: {:,} downloading with {} and {}"
      .format(number_of_abstract, querykey, webenv))

# number_of_abstract = 10
# number_of_abstract = 20
number_of_abstract = 60
# number_of_abstract = 1000

# retmax = 10000
# retmax = 5000
# retmax = 1000
retmax = 20
# retmax = 10

with open(out_filename, 'w') as json_out_file:
    result = eutils.efetch(json_out_file, number_of_abstract,
                           querykey, webenv, retmax)
if result[2] > 0:
    print("\nNo. of article with no abstract: {}".format(result[2]))
print("\nTotal number of downloads: {}".format(result[1]))
print("\nTotal number of abstracts: {}".format(result[0]))
