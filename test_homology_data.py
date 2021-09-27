import homology_data

def test_no_gene_entry():
    data = {}
    result = homology_data.generate_relationships(data)
    assert result == {}

def test_single_gene_entry():
    data = {'141244': {'7955'}}
    result = homology_data.generate_relationships(data)
    assert result == {}

def test_multiple_gene_entries():
    data = {'3' : sorted({'34', '11364', '38864', '406283'}, key = int)}
    result = homology_data.generate_relationships(data)
    assert len(result) == 1
    k, itr = result.popitem()
    assert k == '3'
    v = list(itr)
    assert len(v) == 6
    assert v[0] == ('34', '11364')
    assert v[1] == ('34', '38864')
    assert v[2] == ('34', '406283')
    assert v[3] == ('11364', '38864')
    assert v[4] == ('11364', '406283')
    assert v[5] == ('38864', '406283')

def test_multiple_groupid_and_gene_entries():
    gene_set_1 = sorted({'102631809','102637524','102639201','102637524'}, key = int)
    gene_set_2 = sorted({'102724657', '622699'}, key = int)
    data = {'141201' : gene_set_1, '141209': gene_set_2}
    result = homology_data.generate_relationships(data)
    assert len(result) == 2
    v = list(result['141201'])
    assert len(v) == 3
    assert v[0] == ('102631809', '102637524')
    assert v[1] == ('102631809', '102639201')
    assert v[2] == ('102637524', '102639201')
    v = list(result['141209'])
    assert len(v) == 1
    assert v[0] == ('622699', '102724657')