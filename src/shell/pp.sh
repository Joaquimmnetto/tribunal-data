#!/usr/bin/env bash


i=0
dest="../.."
num_prod=3
chat_csv=chat.csv
chat_corpus=chat_corpus.txt
players=False
matches=False

for dir in `ls ../../dataset/*/ -d`
do

    echo "Processing dir $dir"
    if [ $i%3==0 ]; then
        python ../python/corpus_builder.py $dir $dest $num_prod $chat_csv $chat_corpus $players $matches
    fi
    let i=$i+1
done

