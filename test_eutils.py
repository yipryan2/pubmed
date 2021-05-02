import eutils
import json
import os
import pytest
import requests
import sys
import tempfile
import time


def test_esearch():
    # Query one article.
    result = eutils.esearch('27870832[pmid]')
    assert result[1] ==  1               # Number of hits.
    assert result[2] == '1'              # Query key.
    assert result[3].startswith('MCID_') # Web env.
    # Query two articles.
    result = eutils.esearch('27870832[pmid] or 28420691[pmid]')
    assert result[1] ==  2               # Number of hits.
    assert result[2] == '1'              # Query key.
    assert result[3].startswith('MCID_') # Web env.
    # Keyword-based query.
    result = eutils.esearch('HIV')
    assert result[1] >  99               # Number of hits.
    assert result[2] == '1'              # Query key.
    assert result[3].startswith('MCID_') # Web env.


def test_esearch_error():
    # Test that a query to the wrong URL raises an error 404.
    with pytest.raises(requests.exceptions.HTTPError) as ex:
        _ = eutils.esearch('HIV', 'https://www.google.com/wrong')
        assert ex.response.status_code == 404


def test_efetch():
    _, _, querykey, webenv = eutils.esearch('HIV')
    with tempfile.TemporaryFile('w+') as tmpf:
        result = eutils.efetch(20, querykey, webenv, retmax=10, outfile=tmpf)
        tmpf.seek(0) # Rewind.
        abstracts_dict = json.load(tmpf)
    assert result[0] == len(abstracts_dict)
    assert result[1] == 20
    assert result[0] + result[2] == 20


def test_efetch_error():
    # Test that a query to the wrong URL raises an error 404.
    with pytest.raises(requests.exceptions.HTTPError) as ex:
        _ = eutils.efetch(10, '1', 'MCID_608d46e325a8b65cf511b0e5',
                 url='https://www.google.com/wrong')
        assert ex.response.status_code == 404
