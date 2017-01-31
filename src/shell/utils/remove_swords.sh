#!/usr/bin/env bash

champs=$(sed 's=.*=\\b&\\b=g' < en_stopwords.txt | tr '\n' '|')
sed -E "s/(^${champs::-1}$)//gI" < ${1} | tr -s " "

