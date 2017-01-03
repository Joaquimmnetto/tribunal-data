smpl_size=1000000
echo "Generating with sample size ${smpl_size}:"
shuf -n ${smpl_size} ${1}/chat.csv > ${1}/samples/chat.csv

echo "Generating models for the sample"
./generate_models.sh 6 ${1}/samples

