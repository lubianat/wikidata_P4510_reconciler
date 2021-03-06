import requests
from collections import defaultdict
from article_id_converter import *

# From https://github.com/lubianat/wikidata_bib/blob/7cb3f95685772bc65138098d484f1e4b208bb208/src/wikidata_bib/helper.py#L27



# Currently limited to 500 results
def get_qids_from_europe_pmc(query, cursor_mark = "*"):
    """
    Pulls a list of Wikidata QIDs ordered by date (newest first) from Europe PMC.
    Args:
      query (str): The query used to search te article repository. 
    """
    params = {"query": query, "format": "json", "pageSize": "300", "cursorMark":cursor_mark, "resultType":"lite"}
    response = requests.get("https://www.ebi.ac.uk/europepmc/webservices/rest/search", params)
    data = response.json()
    pmids = []

    for article in data["resultList"]["result"]:
        try:
            pmid = article["pmid"]
            pmids.append(pmid)
        except:
            continue
      
    qids = convert_ids(pmids, input_id="PMID", output_id="QID")
    valid_qids = [i for i in qids if i!=""]
    print(f"{str(len(valid_qids))} qids were found")

    
    if "nextCursorMark" in data and len(data["resultList"]["result"])>0:
      qids.extend(get_qids_from_europe_pmc(query, cursor_mark = data["nextCursorMark"]))
      
    return qids


def get_qids_from_NCBI(query):
    """
    Pulls a list of Wikidata QIDs ordered by date (newest first) from NCBI PMC.
    Args:
      query (str): The query used to search te article repository. 
    """
    params = {"term": query, "format": "json"}
    response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&retmax=500", params)
    data = response.json()      
   
    pmids = []

    for article in data["esearchresult"]["idlist"]:
        try:
            pmid = article
            pmids.append(pmid)
        except:
            continue

    qids = convert_ids(pmids, input_id="PMID", output_id="QID")
    return qids