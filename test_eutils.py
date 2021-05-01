import json
import time
import tempfile
import pytest
import eutils


@pytest.fixture
def eutils_options():
    # make sure we do not over the 3 requests per second limit
    time.sleep(1)
    eutils_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    esearch_param = 'esearch.fcgi?db=pubmed&term=hiv+or+aids&usehistory=y&retmode=json'
    return {
        'esearch_expected_url': eutils_url + esearch_param,
        'error_url': 'https://www.google.com/nothere',
        'query': "hiv or aids",
    }


def test_esearch(eutils_options):
    result = eutils.esearch(eutils_options['query'])
    assert len(result) == 4
    assert result[0] == eutils_options['esearch_expected_url']
    assert result[1] >= 493709
    assert result[2] == '1'
    assert result[3][0:5] == 'MCID_'


def test_esearch_error(eutils_options):
    with pytest.raises(SystemExit) as exc_info:
        _ = eutils.esearch(eutils_options['query'],
                           eutils_options['error_url'])
    assert exc_info.value.args[0].response.status_code == 404


def test_efetch(eutils_options):
    result = eutils.esearch(eutils_options['query'])
    number_of_abstract = 20
    querykey = result[2]
    webenv = result[3]
    retmax = 10
    with tempfile.TemporaryFile(mode='w+') as out_file:
        result = eutils.efetch(out_file, number_of_abstract,
                               querykey, webenv, retmax)
        # read it back after write
        out_file.seek(0)
        abstracts_dict = json.load(out_file)
    assert number_of_abstract == result[1]
    assert len(abstracts_dict) == result[0]


def test_efetch_error(eutils_options):
    number_of_abstract = 20
    querykey = '1'
    webenv = 'MCID_608d46e325a8b65cf511b0e5'
    retmax = 10
    with tempfile.TemporaryFile(mode='w+') as out_file:
        with pytest.raises(SystemExit) as exc_info:
            _ = eutils.efetch(out_file, number_of_abstract,
                              querykey, webenv, retmax,
                              eutils_options['error_url'])
        assert exc_info.value.args[0].response.status_code == 404
