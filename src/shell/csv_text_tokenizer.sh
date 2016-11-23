#!/usr/bin/env bash

#awk -F "," '{print $6}' < $1 | tr A-Z a-z | tr -sc 'a-z0-9\n' ' '
tmp_file=$(mktemp)

awk -F "," '{print $6}' < $1 > ${tmp_file}
./text_tokenizer.sh $tmp_file

rm ${tmp_file}



