# https://github.com/lubianat/article_id_converter
from helper import *
# https://github.com/lubianat/wdcuration
from wdcuration import today_in_quickstatements, render_qs_url
def main():
  query = '(METHODS:"OpenSim")'
  software_qid = "Q2038919"
  print("--------")
  qids = get_qids_from_europe_pmc(query)

  qs = ""

  for qid in qids:
    if "Q" in qid:
      qs+= f"""
    {qid}|P4510|{software_qid}|S887|Q112254021|S248|Q5412157|S813|{today_in_quickstatements()}"""
  print(render_qs_url(qs))
if __name__ == "__main__":
  main()