FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG='en_US.UTF-8'

COPY requirements.txt  .
RUN pip3 -q install --upgrade pip && pip3 -q install -r requirements.txt

WORKDIR /home/pubmed
COPY refseq.py .
COPY data .

RUN groupadd -g 1000 -r pubmed \
    && useradd -u 1000 -d /home/pubmed -s /bin/bash -g pubmed pubmed
RUN chown -hR pubmed:pubmed /home/pubmed

USER pubmed
