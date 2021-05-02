import calendar
import json
import operator
import requests
import sys
import time
import xml.dom.minidom


def esearch(query, url=None):
    if not url:
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    param = {
        'db'        : 'pubmed',
        'term'      : query,
        'usehistory': 'y',
        'retmode'   : 'json',
    }
    response = requests.get(url, param)
    response.raise_for_status()
    out = response.json()['esearchresult']
    return response.url, int(out['count']), out['querykey'], out['webenv']


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
    # FIXME: Here 'Exception' is way to general. You need to catch
    # the exact exception that corresponds to the fact that there
    # is no pubdate. My guess is that it is an IndexError. Please
    # confirm and update the code.
    except Exception:
        pass
    return " ".join(pubdate)


def efetch(count, querykey, webenv, retmax=10, url=None, outfile=sys.stdout):
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
    for retstart in range(0, count, retmax):
        param['retstart'] = retstart
        # Try the same GET request up to three
        # times and wait 10 seconds in between.
        article_set = None
        for i in range(3):
            response = requests.get(url, param)
            response.raise_for_status()
            # Parse the results with XML document object model.
            dom = xml.dom.minidom.parseString(response.content)
            topnode = dom.getElementsByTagName('PubmedArticleSet')
            if not topnode:
                error_string = dom.getElementsByTagName('ERROR')[0].firstChild.data
                raise Exception(error_string)
            article_set = dom.getElementsByTagName('PubmedArticle')
            if not article_set:
                sys.stderr.write("GET failure. Retry after 10 seconds.\n")
                time.sleep(10)
            else:
                break
        if not article_set:
            raise Exception('Three GET failures.')
        sys.stderr.write("{:,} articles have been downloaded.\n".format(len(article_set)))
        number_of_download += len(article_set)
        sys.stderr.write("A total of {:,} articles have been downloaded.\n".format(number_of_download))
        for article in article_set:
            article_dict = {}
            pmid = article.getElementsByTagName('PMID')[0].firstChild.data
            date_elements = article.getElementsByTagName('ArticleDate') or \
                            article.getElementsByTagName('PubDate')
            article_dict['Date'] = get_pubdate(date_elements[0].childNodes)
            article_dict['Title'] = get_text(article.getElementsByTagName('ArticleTitle')[0])
            article_dict['Abstract'] = get_abstracts(article.getElementsByTagName('AbstractText'))
            if article_dict['Abstract']:
                abstract_dict[pmid] = article_dict
            else:
                no_abstract_list.append(pmid)

        sys.stderr.write("A total of {:,} abstracts have been parsed.\n".format(len(abstract_dict)))
        if count > retstart:
            time.sleep(2)
    abstract_dict = dict(sorted(abstract_dict.items(), key=operator.itemgetter(0)))
    json.dump(abstract_dict, outfile, ensure_ascii=False, indent=4, sort_keys=False)
    return len(abstract_dict), number_of_download, len(no_abstract_list)
