#!/bin/sh

test_description="Test shell Python commands for generating collision reports"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

tmp_dir=$(mktemp -d)

. $DIR/sharness.sh

cp $DIR/data/example.* ${tmp_dir}/.
cd $tmp_dir

test_expect_success "Can parse example.fa.gz and generate expected report" "
    $DIR/../process_mgnify_fasta.py example.fa.gz &&
    gunzip example.csv.gz &&
    diff ${DIR}/data/expected.example.csv example.csv &&
    echo success
"

test_expect_success "Can parse problematic csv and report issues" "
    $DIR/../compare.py ${DIR}/data/example.problematic.csv.gz report.csv &&
    diff ${DIR}/data/expected.problematic.report.csv report.csv &&
    echo success
"

test_done
