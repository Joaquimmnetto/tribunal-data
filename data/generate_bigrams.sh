#!/usr/bin/env bash

csv_col=${1}
dir=${2}
min_freq=${3}

echo "Bigrams uses chat files generated for unigram models"
tkn_corpus_uni=${dir}/chat_tkn.crp
tkn_corpus=${dir}/chat_tkn.crp
tkn_vocab=${dir}/bigrams/chat_tkn.vocab

echo "Creating base files..."
./qpy.sh bigram_builder.py model_dir:${dir}
./qsh.sh build_vocab.sh ${tkn_corpus} > ${tkn_vocab}

cp ${dir}/chat.csv ${dir}/bigrams/chat.csv
cp ${dir}/players.csv ${dir}/bigrams/players.csv
cp ${dir}/matches.csv ${dir}/bigrams/matches.csv


./generate_models.sh ${csv_col} ${dir}/bigrams ${min_freq} true















