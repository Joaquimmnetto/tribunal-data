#!/usr/bin/env bash

champs=$(sed 's=.*=\\b&\\b=g' < champs.txt | tr '\n' '|')
sed -E "s/(^${champs::-1}$)/champname/gI" < ${1} | tr -s " "

