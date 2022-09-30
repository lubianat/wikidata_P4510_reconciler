# https://github.com/lubianat/article_id_converter
from helper import *
import click
from pathlib import Path
from time import gmtime, strftime

def today_in_quickstatements():
    return strftime("+%Y-%m-%dT00:00:00Z/11", gmtime())

HERE = Path(__file__).parent.resolve()

def render_quickstatements_for_software(software_name, software_qid):
  """
  Saves a file with the Quickstatements commands to tag articles that use a given piece of software. 

  May be applied to other things that are "used" (e.g. equipment and reagents)
  Args:
    software_name (str): The name of the software to be searched on EuropePMC. Should be unambiguous. 
    software_qid (str): The Wikidata QID for the target topic. 
  """
  query = f"(METHODS:'{software_name}')"
  query_url = f"https://europepmc.org/search?query={query}"
  print("--------")
  qids = get_qids_from_europe_pmc(query)
  valid_qids = [i for i in qids if i!=""]
  print(f"{str(len(valid_qids))} qids were found")
  qs = ""

  for qid in qids:
    if "Q" in qid:
      qs+= f"""
{qid}|P4510|{software_qid}|S887|Q112254021|S248|Q5412157|S813|{today_in_quickstatements()}|S854|"{query_url}" """

  return(qs)

@click.command()
@click.argument('software_name')
@click.argument('software_qid')
@click.option('--filename', default="quickstatements.qs", help='The filename to be generated.')
def main(software_name, software_qid, filename):
  qs = render_quickstatements_for_software(software_name, software_qid)
  HERE.parent.joinpath(filename).write_text(qs)

if __name__ == "__main__":
  main()