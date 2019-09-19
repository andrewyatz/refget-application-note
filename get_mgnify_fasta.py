#!/usr/bin/env python3

import sys
import requests
import os.path
from os import path

def process_file(file_number):
  mgnify_root='http://ftp.ebi.ac.uk/pub/databases/metagenomics/peptide_database/2019_05'
  target="{}/mgy_proteins_{}.fa.gz".format(mgnify_root, file_number)
  download_file(target)

def download_file(url):
  local_filename = url.split('/')[-1]

  if(path.exists(local_filename)):
    print("Cannot proceed. Local file '{}' already exists".format(local_filename), file=sys.stderr)
    sys.exit(1)

  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
      for chunk in r.iter_content(chunk_size=8192):
        if chunk: # filter out keep-alive new chunks
          f.write(chunk)
  return local_filename

def main():
  if(len(sys.argv) != 2):
    print("Please provide the MGnify file number to download and process", file=sys.stderr)
    sys.exit(0)
  file_number=int(sys.argv[1])
  process_file(file_number)

if __name__ == '__main__':
  main()
