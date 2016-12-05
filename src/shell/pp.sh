#!/usr/bin/env bash


i=0

dest="../.."
num_prod=3
chat_csv=chat_offender.csv
chat_corpus=None
players=None
matches=None

executable='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   executable='python3'
fi

for dir in `ls ../../dataset/*/ -d`
do
    echo "Processing dir $dir"
    if [ $i%3==0 ]; then
        $executable ../python/corpus_builder.py $dir $dest $num_prod $chat_csv $chat_corpus $players $matches
    fi
    let i=$i+1
done

