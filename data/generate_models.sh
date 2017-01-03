#!/usr/bin/env bash


sh_dir=../src/shell
py_dir=../src/python

csv_col=${1}
dir=${2}
csv=${dir}/chat.csv


pyexec='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   pyexec='python3'
fi

echo "Creating corpus, tokenizing and extracting vocabulary..."
corpus=${dir}/chat.crp
tkn_corpus=${dir}/chat_tkn.crp
tkn_vocab=${dir}/chat_tkn.vocab
${sh_dir}/csv_text_extractor.sh ${csv_col} ${csv} > ${corpus}
${sh_dir}/text_tokenizer.sh ${corpus} > ${tkn_corpus}
${sh_dir}/build_vocab.sh ${tkn_corpus} > ${tkn_vocab}

echo "Creating the .pkl files corresponding to the vocabulary"
pkl_vocab=${dir}/vocab_freq.pkl
pkl_words=${dir}/words.pkl
min_freq=50
${pyexec} ${py_dir}/sentence_generator/vocab_builder.py ${tkn_vocab} ${pkl_vocab} ${pkl_words} ${min_freq}

echo "Creating the w2v model"
w2v_tkn_model=${dir}/w2v_model.bin
${pyexec} ${py_dir}/context_corrector/w2v_builder.py ${tkn_corpus} ${w2v_tkn_model} ${min_freq}

echo "Creating the errors and corrections dict"
max_dist=0.5
min_sim=0.60
syn_out=${dir}/corrector_dict.pkl
err_out=${dir}/error_dict.pkl
${pyexec} ${py_dir}/context_corrector/corrector_builder.py ${pkl_vocab} ${w2v_tkn_model} ${max_dist} ${min_sim} ${syn_out} ${err_out}
