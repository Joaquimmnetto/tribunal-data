#!/usr/bin/env bash

csv_col=${1}
dir=${2}
min_freq=${3}

sh_dir=../src/shell
py_dir=../src/python

pyexec='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   pyexec='python3'
fi

tkn_corpus_uni=${dir}/chat_tkn.crp
tkn_corpus=${dir}/chat_tkn.crp
tkn_vocab=${dir}/bigrams/chat_tkn.vocab

echo "Creating base files..."
${pydir}/utils/bigram_builder.py model_dir:${dir}
${sh_dir}/utils/build_vocab.sh ${tkn_corpus} > ${tkn_vocab}
cp ${dir}/players.csv ${dir}/bigrams/players.csv
cp ${dir}/matches.csv ${dir}/bigrams/matches.csv

./generate_models.sh ${csv_col} ${1}/bigrams ${min_freq} true















