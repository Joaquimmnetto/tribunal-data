#!/usr/bin/env bash


i=0

dest="../.."
num_prod=6
chat_csv=chat_033.csv
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
        $executable ../python/corpus/corpus_builder.py $dir $dest $num_prod $chat_csv $chat_corpus $players $matches
        if [ $chat_csv!=None ]; then
            sort -t\; -k 1,1n -k 2,2n ${dest}/${chat_csv} > ${dest}/${chat_csv}
        fi
        if [ $players!=None ]; then
            sort -t\; -k 1,1n -k 2,2n ${dest}/${players} > ${dest}/${players}
        fi
        if [ $matches!=None ]; then
            sort -t\; -k 1,1n -k 2,2n ${dest}/${matches} > ${dest}/${matches}
        fi
    fi
    let i=$i+1
done

