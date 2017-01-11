smpl_size=10000
echo "Generating with sample size ${smpl_size}:"

#Mudar depois: pegar a partida, e depois os chats e os jogadores daquela partida.
offset=$(( ( RANDOM %  1000)  + 1 ))
tail --lines=${offset} matches.csv | head -${smpl_size}
#python3 generate_samples.py matches.csv
#tail --lines=${offset} chat.csv | head -${smpl_size}

#shuf -n ${smpl_size} ${1}/chat.csv > ${1}/samples/chat.csv

echo "Generating models for the sample"
./generate_models.sh 6 ${1}/samples

