#!/usr/bin/env python3

import sys
import gzip
import os.path
from os import path
import base64
import hashlib
import binascii
import re

def process_file(file):
  if(path.exists(file) == False):
    print("Cannot continue because {} does not exist".format(file), file=sys.stderr)
    sys.exit(1)

  output_file = file.replace(".fa.gz", ".csv.gz")
  p = re.compile(">(.+?)\s")

  if(path.exists(output_file)):
    print("Cannot continue because {} exists".format(output_file), file=sys.stderr)
    sys.exit(1)

  with gzip.open(file, 'rt') as f:
    with gzip.open(output_file, 'wt') as out:
      header = f.readline()
      seq = f.readline().rstrip()

      while header:
        m = p.match(header)
        if m:
          id = m.group(1)
          trunc512 = trunc512_digest(seq)
          md5 = md5_digest(seq)
          print("{},{},{},{}".format(id, trunc512, md5, seq), file=out)
        else:
          print("Skipping line '{}' because it did not parse correctly".format(header))
        header = f.readline()
        seq = f.readline().rstrip()

def trunc512_digest(seq, offset=24):
  digest = hashlib.sha512(seq.encode('utf-8')).digest()
  hex_digest = binascii.hexlify(digest[:offset])
  return hex_digest.decode('utf-8')

def md5_digest(seq):
  digest = hashlib.md5(seq.encode('utf-8')).digest()
  hex_digest = binascii.hexlify(digest)
  return hex_digest.decode('utf-8')

def main():
  if(len(sys.argv) != 2):
    print("Please provide the MGnify FASTA file to process")
    sys.exit(0)
  process_file(sys.argv[1])

if __name__ == '__main__':
  main()
