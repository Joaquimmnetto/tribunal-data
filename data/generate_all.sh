#!/usr/bin/env bash
#set +e
csv_col=6
min_freq=800 #~21k palavras
min_freq_smpl=70 #~10k bigramas

echo "Creating base files..."
#./generate_samples.sh full
#./extract_team.sh ally
#./extract_team.sh enemy
#./extract_team.sh offender

echo "Generating samples..."


./generate_models.sh ${csv_col} full/samples 5 false
./generate_models.sh ${csv_col} ally/samples 5 false
./generate_models.sh ${csv_col} enemy/samples 5 false
./generate_models.sh ${csv_col} offender/samples 5 false

./generate_bigrams.sh ${csv_col} full/samples ${min_freq_smpl}
./generate_bigrams.sh ${csv_col} ally/samples ${min_freq_smpl}
./generate_bigrams.sh ${csv_col} enemy/samples ${min_freq_smpl}
./generate_bigrams.sh ${csv_col} offender/samples ${min_freq_smpl}

echo "Generating full models"
./generate_models.sh ${csv_col} full ${min_freq} false
./generate_bigrams.sh ${csv_col} full ${min_freq}

./generate_models.sh ${csv_col} ally ${min_freq} false
./generate_bigrams.sh ${csv_col} ally ${min_freq}

./generate_models.sh ${csv_col} enemy ${min_freq} false
./generate_bigrams.sh ${csv_col} enemy ${min_freq}

./generate_models.sh ${csv_col} offender ${min_freq} false
./generate_bigrams.sh ${csv_col} offender ${min_freq}

echo "Generating clustering results"
./analise_lda.sh
./analise_clusters.sh

















