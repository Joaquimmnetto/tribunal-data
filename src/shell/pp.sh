#!/usr/bin/env bash

i=0
dest="../.."
num_prod=2

for dir in `ls ../../dataset/*/ -d`
do
    echo "Processing dir $dir"
    if [ $i%1==0 ]; then
        python ../python/corpus_builder.py $dir $dest $num_prod
    fi
    let i=$i+1
done

