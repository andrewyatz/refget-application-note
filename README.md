# refget-application-note

Code associated with refget application note

## Setup

```
pip install -r requirements.txt
```

## MGnify hash clash analysis

The following pipeline requires a minimum of 500GB of disk space. MGnify downloads total 136GB, intermediate compressed CSV files are 190GB and final sorted CSV file is ~170GB.

### Processing MGnify FASTA files

Downloading and processing a single MGnify protein file into a compressed CSV file where columns are:

- id
- trunc512 checksum
- md5 checksum
- protein sequence

The following command should be repeated for each file you wish to download from May 2019 the MGnify protein set.

```bash
./get_mgnify_fasta.py 6
./process_mgnify_fasta.py mgy_proteins.fa.gz
```

Analysing trunc512 checksums can be achieved by first creating an intermediary format using awk where the columns are:

- checksum (trunc512)
- protein sequence
- id

### Sorting MGnify checksums

```bash
# Processing trunc512
mkdir tmpsort
gzip -dc mgy_proteins_*.csv.gz | awk -F "," -v OFS=',' '{print $2,$4,$1}' | sort -k1,1 --temporary-directory=$PWD/tmpsort | gzip -c > trunc512.csv.gz
./compare.py trunc512.csv.gz trunc512.report.csv
```

We sort the new format by the 1st column (trunc512 checksum). These files will be very big so when we allow sort to use `$PWD/tmpsort` as an intermediate sorting area as `$TMPDIR` is unlikely to be large enough.

### Finding clashing checksums

`compare.py` then scans the sorted list looking for checksum identity where underlying sequences are not identical. All clashing elements are reported back to output csv file where columns are:

- Problematic checksum
- Identifier 1
- Sequence 1
- Identifier 2
- Sequence 2

An empty final file means no issues were found with the checksummed data. If you wish to see what the program should emit when given clashing identifiers you can run `./compare.py example.problematic.csv output.csv`.
