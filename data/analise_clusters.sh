#!/usr/bin/env bash

echo "LDA for enemy:"
model_dir=model_dir:enemy
out_dir=analise
echo "LDA for enemy and 2 topics"
#./qpy.sh lda_builder.py ${model_dir} num_topics:2 lda_team:${out_dir}/lda_enemy_2.gsm lda_team_csv:${out_dir}/lda_enemy_2.csv > ${out_dir}/lda_enemy_2.txt
echo "LDA for enemy and 3 topics"
#./qpy.sh lda_builder.py ${model_dir} num_topics:3 lda_team:${out_dir}/lda_enemy_3.gsm lda_team_csv:${out_dir}/lda_enemy_3.csv > ${out_dir}/lda_enemy_3.txt

echo "LDA for offender:"
model_dir=model_dir:offender
out_dir=analise
echo "LDA for offender and 4 topics"
#./qpy.sh lda_builder.py ${model_dir} num_topics:4 lda_team:${out_dir}/lda_offender_4.gsm lda_team_csv:${out_dir}/lda_offender_4.csv > ${out_dir}/lda_offender_4.txt
echo "LDA for offender and 6 topics"
#./qpy.sh lda_builder.py ${model_dir} num_topics:6 lda_team:${out_dir}/lda_offender_6.gsm lda_team_csv:${out_dir}/lda_offender_6.csv > ${out_dir}/lda_offender_6.txt


#full: 2, 3?
echo "KMN for full"
model_dir=model_dir:full
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 
#ally: 3, 6
echo "KMN for ally"
model_dir=model_dir:ally
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:6 
#enemy: 2, 3
echo "KMN for enemy"
model_dir=model_dir:enemy
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 
#offender: 4, 6
echo "KMN for offender"
model_dir=model_dir:offender
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:4 
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:6 


echo "KMN for full-bigrams"
#full-bigram:2, 3
model_dir=model_dir:full/bigrams
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 
#ally-bigram: 6, 9
echo "KMN for ally-bigrams"
model_dir=model_dir:ally/bigrams
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:6 
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:9 
#enemy-bigram: 2, 3?
echo "KMN for enemy-bigrams"
model_dir=model_dir:enemy/bigrams
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 
# offender-bigrams: 2,3?
echo "KMN for offender-bigrams"
model_dir=model_dir:offender/bigrams
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 

