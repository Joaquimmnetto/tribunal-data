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
${sh_dir}/utils/csv_text_extractor.sh ${csv_col} ${csv} > ${corpus}
${sh_dir}/utils/text_tokenizer.sh ${corpus} > ${tkn_corpus}
${sh_dir}/utils/build_vocab.sh ${tkn_corpus} > ${tkn_vocab}

echo "Creating the .pkl files corresponding to the vocabulary"
#pkl_vocab=${dir}/vocab_freq.pkl
#pkl_words=${dir}/words.pkl
min_freq=0
${pyexec} ${py_dir}/utils/vocab_builder.py ${dir} ${dir} ${min-freq}

echo "Creating the w2v model"
#w2v_tkn_model=${dir}/w2v_model.bin
${pyexec} ${py_dir}/utils/w2v_builder.py ${dir} ${dir} ${min_freq}

echo "Creating the errors and corrections dict"
max_dist=0.5
min_sim=0.60
#syn_out=${dir}/corrector_dict.pkl
#err_out=${dir}/error_dict.pkl
${pyexec} ${py_dir}/utils/err_dict_builder.py ${dir} ${max_dist} ${min_sim} ${dir}
