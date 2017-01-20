#!/usr/bin/env bash

#remover stopwords
sed -f <(sed 's/.*/s|\\\<&\\\>||g/' ${2}) < ${1}
