# refget-application-note

Code associated with refget application note

## Setup

```
pip install -r requirements.txt
```

## MGnify hash clash analysis

Downloading and processing a single MGnify protein file into a CSV file where columns are:

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

```bash
# Processing trunc512
mkdir tmpsort
cat mgy_proteins_*.csv | awk -F "," -v OFS=',' '{print $2,$4,$1}' | sort -k1,1 --temporary-directory=$PWD/tmpsort > trunc512.csv
./compare.py trunc512.csv trunc512.report.csv
```

We sort the new formatby the 1st column (trunc512 checksum). These files will be very big so we allow sort to store intermediate sorted files locally as default TMPDIR is unlikely to be large enough.

`compare.py` then scans the sorted list looking for checksum identity where underlying sequences are not identical. All clashing elements are reported back to output csv file where columns are:

- Problematic checksum
- Identifier 1
- Sequence 1
- Identifier 2
- Sequence 2

An empty final file means no issues were found with the checksummed data. If you wish to see what the program should emit when given clashing identifiers you can run `./compare.py example.problematic.csv output.csv`.
