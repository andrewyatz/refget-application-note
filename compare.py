#!/usr/bin/env python3

import sys
import os.path
import gzip
from os import path

def process_file(file, output_file):
  if(path.exists(file) == False):
    print("Cannot continue because {} does not exist".format(file), file=sys.stderr)
    sys.exit(1)
  if(path.exists(output_file) == True):
    os.remove(output_file)

  with gzip.open(file, 'rt', encoding='utf-8') as f:
    with open(output_file, 'w', encoding='utf-8') as output:
      previous = []
      # Expected format input is
      # checksum,sequence,identifier
      for line in f:
        current = line.rstrip().split(',')
        if previous:
          if(current[0] == previous[0]): # check checksums match
            if(current[1] != previous[1]): # check if the seqs do not match
              # Expected format output is
              # clashed_checksum,identifier_one,seq_one,identifier_two,seq_two
              print("{},{},{},{},{}".format(previous[0], previous[2], previous[1],
                current[2], current[1]), file=output)
        previous = current

def main():
  if(len(sys.argv) != 3):
    print("Please provide the commpressed sorted comma separated file to process and output file")
    print("./compare.py input.csv.gz report.csv")
    sys.exit(0)
  process_file(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
  main()
