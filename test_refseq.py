import refseq

def test_format_date():
    assert refseq.format_date("20210611") == '2021-06-11'

def test_external_identifiers_basic():
    result = refseq.external_identifiers('MIM:138670|HGNC:HGNC:5|Ensembl:ENSG00000121410') 
    assert result["OMIM_ID"] == 138670
    assert result["Ensembl_ID"] ==  'ENSG00000121410'

def test_external_identifiers_flybase():
    result = refseq.external_identifiers('FLYBASE:FBgn0261446')
    assert result["FlyBase_ID"] == 'FBgn0261446'
