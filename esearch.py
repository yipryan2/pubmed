#!/usr/bin/env python3

import eutils

query = "hiv or aids"

result = eutils.esearch(query)

print("\nesearch command:\n" + result[0] + "\n")
print("Number of abstract={}, querykey={} and webenv={}"
      .format(result[1], result[2], result[3]))
