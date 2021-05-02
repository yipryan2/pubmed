#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
python download_abstracts.py 'hiv or aids' > pubmed-data.json
'''


import eutils
import sys

query = sys.argv[1]

_, count, querykey, webenv = eutils.esearch(query)
a, b, c = eutils.efetch(count, querykey, webenv, retmax=10)

sys.stderr.write(f'{a} {b} {c}\n')
