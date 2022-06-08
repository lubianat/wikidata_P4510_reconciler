# https://github.com/lubianat/article_id_converter
import webbrowser
from helper import *
# https://github.com/lubianat/wdcuration
from wdcuration import today_in_quickstatements, render_qs_url
import click

def render_quickstatements_for_software(software_name):
  query = "(METHODS:'OpenSim')"
  query_url = f"https://europepmc.org/search?query={query}"
  software_qid = "Q2038919"
  print("--------")
  qids = get_qids_from_europe_pmc(query)
  valid_qids = [i for i in qids if i!=""]
  print(f"{str(len(valid_qids))} qids were found")
  qs = ""

  for qid in qids:
    if "Q" in qid:
      qs+= f"""
    {qid}|P4510|{software_qid}|S887|Q112254021|S248|Q5412157|S813|{today_in_quickstatements()}|S854|"{query_url}" """
    break
  return(qs)

@click.command()
@click.argument('name')
def main(name):
  qs = render_quickstatements_for_software(name)
  webbrowser.open(render_qs_url(qs))
if __name__ == "__main__":
  main()