#!/usr/bin/env bash
pyexec='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   pyexec='python3'
fi

utils_dir=../src/shell/utils

smpl_size=30000
echo "Generating with sample size ${smpl_size}:"
rm ${1}/samples/matches.csv
shuf -n ${smpl_size} ${1}/matches.csv > ${1}/samples/matches.csv

echo "Sorting input files...:"
echo "Matches sample..."
${utils_dir}/sort_csv.sh ${1}/samples/matches.csv ${1}/samples/sorted_matches.csv
mv ${1}/samples/sorted_matches.csv ${1}/samples/matches.csv

echo "Players"
${utils_dir}/sort_csv.sh ${1}/players.csv ${1}/sorted_players.csv
mv ${1}/sorted_players.csv ${1}/players.csv

echo "Chat"
${utils_dir}/sort_csv.sh ${1}/chat.csv ${1}/sorted_chat.csv
mv ${1}/sorted_chat.csv ${1}/chat.csv

echo "Generating players and chat samples"
${pyexec} ../src/python/utils/generate_samples.py model_dir:${1}

