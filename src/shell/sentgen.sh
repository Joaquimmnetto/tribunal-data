#!/usr/bin/env bash


executable='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   executable='python3'
fi
echo Executing Tokenizer...
$executable ../python/unicode_tokenizer.py ${1} > tmp/token.tmp
#./text_tokenizer.sh ${1} > tmp/token.tmp
echo Building vocabulary...
./build_vocab.sh tmp/token.tmp > tmp/vocab.tmp

fname=out/$(basename ${1})
echo Building vocabulary model...
$executable ../python/sentence_generator/vocab_builder.py tmp/vocab.tmp /dev/null ${fname}_words.pkl 0

echo Building neighbor model...
$executable ../python/sentence_generator/context_builder.py tmp/token.tmp ${fname}_words.pkl ${fname}_neigh.spy ${fname}_fw.pkl
