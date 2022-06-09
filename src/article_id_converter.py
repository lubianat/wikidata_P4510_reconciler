import requests
from collections import defaultdict

# Function from https://github.com/lubianat/article_id_converter

def convert_ids(list_of_ids, input_id="DOI", output_id="PMCID", return_type="list"):
    """
    Obtains a list of output IDs from Wikidata given a list of input IDs.
    Args:
        list_of_ids (list): A list of IDs as strings.
        input_id (str): The kind of IDs in the input. One of ["PMID", "PMCID", "QID" or "DOI"]
        output_id (str): The kind of IDs to be returned in the output. One of ["PMID", "PMCID", "QID" or "DOI"]
        return_type (str): One of "list" or "data.frame". If "DataFrame", the output includes a column with the input data.

    Returns:
        (list): A list with the target IDs.
        OR
        (DataFrame): A pandas DataFrame
    """
    print(f"===== {str(len(list_of_ids))} identifiers to convert ======")
    id2property = {"PMCID": "P932", "DOI": "P356", "PMID": "P698"}
    values = ""

    list_of_ids = [str(i).upper() for i in list_of_ids]
    if input_id == "QID":
        for id in list_of_ids:
            values = values + f' "wd:{id}"'
        middle_logic = f"""
         ?input_id_temp wdt:{id2property[output_id]} ?output_id_temp .
         """
    else:
        for id in list_of_ids:
            values = values + f' "{id}"'

        if output_id == "QID":
            middle_logic = f"""
         ?output_id_temp wdt:{id2property[input_id]} ?input_id_temp .
         """
        else:

            middle_logic = f"""
         ?item wdt:{id2property[input_id]} ?input_id_temp .
         ?item wdt:{id2property[output_id]} ?output_id_temp .
         """

    query = f"""
    SELECT 
      (REPLACE(STR(?input_id_temp), ".*Q", "Q") AS ?input_id) 
      (REPLACE(STR(?output_id_temp), ".*Q", "Q") AS ?output_id) 
    WHERE 
    {{
      VALUES ?input_id_temp {{ {values} }} .
      {middle_logic}
    }}
    """

    endpoint_url = "https://query.wikidata.org/sparql"

    response = requests.get(
        endpoint_url,
        params={"query": query, "format": "json"},
        headers={"User-Agent": "article id converter"},
    )
    query_result = response.json()

    def def_value():
        return ""

    mappings = defaultdict(def_value)
    for i in query_result["results"]["bindings"]:

        mappings[i["input_id"]["value"]] = i["output_id"]["value"]

    return [mappings[k] for k in list_of_ids]
