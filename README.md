# pubmed

[![Build Status](https://github.com/yipryan2/pubmed/workflows/PubMed-CI/badge.svg?branch=main)](https://github.com/yipryan2/pubmed/actions)

Extract abstracts from PubMed

## Using Docker to run this script

To build

```shell
git clone <https://github.com/yipryan2/pubmed.git>
cd pubmed
docker build -t pubmed:0.1 .
```

To run

```shell
docker run --rm -it pubmed:0.1
```
