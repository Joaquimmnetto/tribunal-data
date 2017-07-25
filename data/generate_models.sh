#!/usr/bin/env bash

csv_col=${1}
dir=${2}
min_freq=${3}
bigram=${4}

echo "args: col:${1}, dir:${2}, min_freq:${3}, bigram:${4}"

echo "Is the model a bigram model? ${bigram}"
echo "Creating model for ${dir}"

wc -l ${dir}/chat.csv
echo "Assuring the cohesion of dataset"
Rscript ../src/R/preprocessing.R ${dir}
wc -l ${dir}/chat.csv

csv=${dir}/chat.csv
swords=en_stopwords.txt
corpus=${dir}/chat.crp
corpus_sw=${dir}/chat_sw.crp
corpus_nosw=${dir}/chat_nosw.crp
tkn_corpus=${dir}/chat_tkn.crp
tkn_vocab=${dir}/chat_tkn.vocab
if [[ "$bigram" == 'false' ]]; then
	echo "Creating corpus, tokenizing and extracting vocabulary..."
	echo "Extracting corpus from csv file"
	./qsh.sh csv_text_extractor.sh ${csv_col} ${csv} > ${corpus}
	echo "Tokenizing corpus"
	./qsh.sh text_tokenizer.sh ${corpus} > ${corpus_sw}
	echo "Removing stopwords"
	./qsh.sh remove_swords.sh ${corpus_sw} > ${corpus_nosw}
	echo "Replacing champ names"
	./qsh.sh replace_champs.sh ${corpus_nosw} > ${tkn_corpus}

	rm ${corpus_sw}
	rm ${corpus_nosw}
	rm ${corpus}
fi

echo "Building vocabulary from corpus"cd ..
./qsh.sh build_vocab.sh ${tkn_corpus} > ${tkn_vocab}

echo "Creating the .pkl files corresponding to the vocabulary"
model_dir=model_dir:${dir}
min_freq=min_freq:${3}
./qpy.sh vocab_builder.py ${model_dir} ${min_freq}

#if [[ "$bigram" == 'false' ]]; then
#	echo "Creating the w2v model"
#	w2v_tkn_model=${dir}/w2v_model.bin
#	${pyexec} ${py_dir}/utils/w2v_builder.py ${model_dir} ${min_freq}

echo "Creating the count matrix"
./qpy.sh count_matrix_builder.py ${model_dir} ${min_freq}

echo "Generating the d2v model"
./qpy.sh d2v_model_builder.py ${model_dir} ${min_freq}

echo "Generating idfs"
./qpy.sh idfs_builder.py ${model_dir}

echo "Generating the lda model by team over bow"
./qpy.sh lda_builder.py ${model_dir}







