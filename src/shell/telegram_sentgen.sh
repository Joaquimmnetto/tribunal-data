#!/usr/bin/env bash


executable='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   executable='python3'
fi

corpus_path=../../dataset/telegram_corpora/

for file in  `ls ${corpus_path}`
do
    echo "Current file ""${file}"
    ./sentgen.sh ${corpus_path}${file}
done