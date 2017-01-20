#!/usr/bin/env bash

sh_dir=../src/shell
py_dir=../src/python

csv_col=${1}
dir=${2}
min_freq=${3}
bigram=${4}

csv=${dir}/chat.csv

pyexec='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   pyexec='python3'
fi
echo "Is the model a bigram model? ${bigram}"

swords=en_stopwords.txt
corpus=${dir}/chat.crp
corpus_sw=${dir}/chat_sw.crp
corpus_nosw=${dir}/chat_nosw.crp
tkn_corpus=${dir}/chat_tkn.crp
tkn_vocab=${dir}/chat_tkn.vocab
if [[ "$bigram" == 'false' ]]; then
	echo "Creating corpus, tokenizing and extracting vocabulary..."
	echo "Extracting corpus from csv file"
	${sh_dir}/utils/csv_text_extractor.sh ${csv_col} ${csv} > ${corpus}
	echo "Tokenizing corpus"
	${sh_dir}/utils/text_tokenizer.sh ${corpus} > ${corpus_sw}
	echo "Removing stopwords"
	${sh_dir}/utils/remove_swords.sh ${corpus_sw}> ${corpus_nosw}
	echo "Removing champ names"
	${sh_dir}/utils/remove_swords.sh ${corpus_nosw}> ${tkn_corpus}
	echo "Building vocabulary from corpus"
	${sh_dir}/utils/build_vocab.sh ${tkn_corpus} > ${tkn_vocab}
fi

echo "Creating the .pkl files corresponding to the vocabulary"
model_dir=model_dir:${dir}
min_freq=min_freq:${3}
${pyexec} ${py_dir}/utils/vocab_builder.py ${model_dir} ${min_freq}

if [[ "$bigram" == 'false' ]]; then
	echo "Creating the w2v model"
	w2v_tkn_model=${dir}/w2v_model.bin
	${pyexec} ${py_dir}/utils/w2v_builder.py ${model_dir} ${min_freq}
	
	echo "Creating the errors and corrections dict"
	max_dist=max_edit_dist:0.5
	min_sim=min_sim:0.55
	${pyexec} ${py_dir}/utils/err_dict_builder.py ${model_dir} ${max_dist} ${min_sim}
fi

echo "Creating the count matrix"
${pyexec} ${py_dir}/utils/count_matrix_builder.py ${model_dir} ${min_freq}

echo "Creating the tfidf matrix"
${pyexec} ${py_dir}/utils/tfidf_matrix_builder.py ${model_dir} ${min_freq}

echo "Generating the d2v model"
${pyexec} ${py_dir}/utils/d2v_model_builder.py ${model_dir} ${min_freq}

echo "Generating the lda model by team over bow"
${pyexec} ${py_dir}/utils/lda_builder.py ${model_dir}

echo "Generating the lsi model by team over tfidf"
${pyexec} ${py_dir}/utils/lsi_builder.py ${model_dir}

echo "Generating the hdp model by team over bow"
${pyexec} ${py_dir}/utils/hdp_builder.py ${model_dir}






