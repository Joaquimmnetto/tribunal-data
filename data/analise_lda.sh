#!/usr/bin/env bash

#full: 2, 3? (5)
#full-bigram:2, 3

#ally: 3, 6(4)
#ally-bigram: 6, 9

#enemy: 2, 3(3)
#enemy-bigram: 2, 3?

#offender: 4, 6(5)
# offender-bigrams: 2,3?


echo "LDA for full:"
model_dir=model_dir:full
out_dir=analise
echo "LDA for full and 5 topics"
./qpy.sh lda_builder.py ${model_dir} num_topics:5 lda_team:${out_dir}/lda_full_5.gsm lda_team_csv:${out_dir}/lda_full_5.csv
./qpy.sh aggregate_clusters.py ${model_dir} n_groups:5 lda:True
./qpy.sh cluster_analysis.py ${model_dir} topic_probs:False lda:True nwords:100 > lda_full_5.txt

echo "LDA for ally:"
model_dir=model_dir:ally
out_dir=analise
echo "LDA for ally and 4 topics"
./qpy.sh lda_builder.py ${model_dir} num_topics:4 lda_team:${out_dir}/lda_ally_4.gsm lda_team_csv:${out_dir}/lda_ally_4.csv
./qpy.sh aggregate_clusters.py ${model_dir} n_groups:4 lda:True
./qpy.sh cluster_analysis.py ${model_dir} topic_probs:False lda:True nwords:100 > lda_ally_4.txt

echo "LDA for enemy:"
model_dir=model_dir:enemy
out_dir=analise
echo "LDA for enemy and 3 topics"
./qpy.sh lda_builder.py ${model_dir} num_topics:3 lda_team:${out_dir}/lda_enemy_3.gsm lda_team_csv:${out_dir}/lda_enemy_3.csv
./qpy.sh aggregate_clusters.py ${model_dir} n_groups:3 lda:True
./qpy.sh cluster_analysis.py ${model_dir} topic_probs:False lda:True nwords:100 > lda_enemy_3.txt

echo "LDA for offender:"
model_dir=model_dir:offender
out_dir=analise
echo "LDA for offender and 5 topics"
./qpy.sh lda_builder.py ${model_dir} num_topics:5 lda_team:${out_dir}/lda_offender_5.gsm lda_team_csv:${out_dir}/lda_offender_5.csv
./qpy.sh aggregate_clusters.py ${model_dir} n_groups:5 lda:True
./qpy.sh cluster_analysis.py ${model_dir} topic_probs:False lda:True nwords:100 > lda_offender_5.txt
