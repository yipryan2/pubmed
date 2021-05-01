import json
import calendar
import time
import operator
import xml.dom.minidom
import requests


def esearch(query, url=None):
    if not url:
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    param = {
        'db'        : 'pubmed',
        'term'      : query,
        'usehistory': 'y',
        'retmode'   : 'json',
    }
    try:
        response = requests.get(url, param)
        response.raise_for_status()
    except Exception as error:
        raise SystemExit(error)
    result = response.json()
    number_of_abstract = int(result['esearchresult']['count'])
    querykey = result['esearchresult']['querykey']
    webenv = result['esearchresult']['webenv']
    return response.url, number_of_abstract, querykey, webenv


def get_text(element):
    text = ""
    for node in element.childNodes:
        if node.nodeType == node.TEXT_NODE:
            text += node.nodeValue
        elif node.nodeType == node.ELEMENT_NODE:
            text += get_text(node)
    return text


def get_abstracts(elements):
    abstract_text_list = []
    for element in elements:
        abstract_text = ""
        if element.hasAttribute('Label'):
            abstract_text = "{}: ".format(element.getAttribute('Label').capitalize())
        abstract_text += get_text(element)
        abstract_text_list.append(abstract_text)
    return abstract_text_list


def get_pubdate(nodes):
    pubdate = []
    for node in nodes:
        if node.nodeType == node.ELEMENT_NODE:
            pubdate.append(node.firstChild.data)
    try:
        month = int(pubdate[1])
        pubdate[1] = calendar.month_abbr[month]
    except Exception:
        pass
    return " ".join(pubdate)


def efetch(out_file, number_of_abstract, querykey, webenv, retmax=10, url=None):
    if not url:
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    param = {
        'db'        : 'pubmed',
        'query_key' : querykey,
        'WebEnv'    : webenv,
        'retstart'  : 0,
        'retmax'    : retmax,
        'retmode'   : 'xml',
        'rettype'   : 'abstract'
    }
    number_of_download = 0
    abstract_dict = {}
    no_abstract_list = []
    for retstart in range(0, number_of_abstract, retmax):
        param['retstart'] = retstart

        for i in range(3):
            try:
                response = requests.get(url, param)
                response.raise_for_status()
            except Exception as error:
                raise SystemExit(error)
            if i == 0:
                print("\nefetch command:\n" + response.url + "\n")

            dom_response = xml.dom.minidom.parseString(response.content)
            article_set = dom_response.getElementsByTagName('PubmedArticleSet')
            if not article_set:
                print("Error: " + dom_response.getElementsByTagName('ERROR')[0].firstChild.data)
                exit()
            article_set = dom_response.getElementsByTagName('PubmedArticle')
            if not article_set:
                print("Fail to download articles. Retry after 10 seconds.", flush=True)
                time.sleep(10)
            else:
                break
        if not article_set:
            print("Fail to download articles after retrying 3 times.")
            exit()
        print("{:,} articles have been downloaded".format(len(article_set)), flush=True)
        number_of_download += len(article_set)
        print("A total of {:,} articles have been downloaded".format(number_of_download), flush=True)
        for article in article_set:
            article_dict = {}
            pmid = article.getElementsByTagName('PMID')[0].firstChild.data
            # print(pmid)
            date_elements = article.getElementsByTagName('ArticleDate')
            if not date_elements:
                date_elements = article.getElementsByTagName('PubDate')
            article_dict['Date'] = get_pubdate(date_elements[0].childNodes)
            article_dict['Title'] = get_text(article.getElementsByTagName('ArticleTitle')[0])
            article_dict['Abstract'] = get_abstracts(article.getElementsByTagName('AbstractText'))
            if article_dict['Abstract']:
                abstract_dict[pmid] = article_dict
            else:
                no_abstract_list.append(pmid)

        print("A total of {:,} articles have been processed".format(len(abstract_dict)), flush=True)
        if number_of_abstract > retstart:
            time.sleep(2)
    abstract_dict = dict(sorted(abstract_dict.items(), key=operator.itemgetter(0)))
    json.dump(abstract_dict, out_file, ensure_ascii=False, indent=4, sort_keys=False)
    return len(abstract_dict), number_of_download, len(no_abstract_list)
