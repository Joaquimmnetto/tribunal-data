#!/usr/bin/env bash
#Builds vocabulary of texts tokenized by text_tokenizer

tr -s ' ' '\n' < $1 | sort | uniq -c | sort -nr | tr -s ' ' ' '