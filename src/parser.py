# https://github.com/lubianat/article_id_converter
from helper import *

def main():
  query = '(METHODS:"OpenSim")'
  software_qid = "Q2038919"
  print("--------")
  qids = get_qids_from_europe_pmc(query)

  qs = ""

  for qid in qids:
    qs+= f"""
  {qid}|P4510|{software_qid}"""


if __name__ == "__main__":
  main()