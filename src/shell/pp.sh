#!/usr/bin/env bash


i=0

dest="../.."
num_prod=12
chat_csv=chat_full.${1}.csv
chat_corpus=corpus_full.${1}.csv
players=players_full.${1}.csv
matches=matches_full.${1}.csv

executable='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   executable='python3'
fi

for dir in `ls ../../dataset/${1}/*/ -d`
do
    echo "Processing dir $dir"
    $executable ../python/corpus/corpus_builder.py $dir $dest $num_prod $chat_csv $chat_corpus $players $matches

done

