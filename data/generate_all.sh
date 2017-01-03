set +e
csv_col=6
echo "Generating samples and models for full"
./generate_samples.sh full
./generate_models.sh ${csv_col} full

echo "Generating samples and models for ally"
./extract_team.sh ally
./generate_models.sh ${csv_col} ally

echo "Generating samples and models for enemy"
./extract_team.sh enemy
./generate_models.sh ${csv_col} enemy

echo "Generating samples and models for offender"
./extract_team.sh offender
./generate_models.sh ${csv_col} offender




