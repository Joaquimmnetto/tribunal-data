#!/usr/bin/env bash

csv_col=${1}
csv=${2}
fname=$(basename "$csv")
bname="${fname%.*}"

echo $bname

pyexec='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   pyexec='python3'
fi

corpus=out/${bname}.crp
tkn_corpus=out/${bname}_tkn.crp
tkn_vocab=out/${bname}_tkn.vocab

./csv_text_extractor.sh ${csv_col} ${csv} > ${corpus}
./text_tokenizer.sh ${corpus} > ${tkn_corpus}
./build_vocab.sh ${tkn_corpus} > ${tkn_vocab}

pkl_vocab=out/${bname}_vocab_freq.pkl
pkl_words=/dev/null
${pyexec} ../python/sentence_generator/vocab_builder.py ${tkn_vocab} ${pkl_vocab} ${pkl_words} 50

w2v_tkn_model=out/${bname}_tkn_w2v.bin
${pyexec} ../python/context_corrector/w2v_builder.py ${tkn_corpus} ${w2v_tkn_model} 50

max_dist=0.5
min_sim=0.60
syn_out=out/${bname}_syn.csv
err_out=out/${bname}_err.csv
${pyexec} ../python/context_corrector/context_corrector.py ${pkl_vocab} ${w2v_tkn_model} ${max_dist} ${min_sim} ${syn_out} ${err_out}
