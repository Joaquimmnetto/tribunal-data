#!/usr/bin/env bash
echo "Extracting ${1}/sample files.."
grep ','"${1}"',' < full/samples/chat.csv > ${1}/samples/chat.csv
cp full/samples/matches.csv ${1}/samples/matches.csv
grep ','"${1}"',' < full/samples/players.csv > ${1}/samples/players.csv

echo "Extracting ${1} files..."
grep ','"${1}"',' < full/chat.csv > ${1}/chat.csv
cp full/matches.csv ${1}/matches.csv
grep ','"${1}"',' < full/players.csv > ${1}/players.csv


