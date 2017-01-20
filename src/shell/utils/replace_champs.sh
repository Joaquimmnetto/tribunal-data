#!/usr/bin/env bash

#remover stopwords
champs=$(tr '\n' '|' < champs.txt)
sed -E "s/(${champs})/champname/gI" < ${1} > ${2}

