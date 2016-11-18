#!/usr/bin/env bash

i=0
fl="../../chat_corpus_sample.txt"

for dir in `ls ../../dataset/*/ -d`
do
    echo "Processing dir $dir"
    if [ $i%20==0 ]; then
        python ../python/corpus_builder.py $dir $fl
    fi
    let i=$i+1
done

