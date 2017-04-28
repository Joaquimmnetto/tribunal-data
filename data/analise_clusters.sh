#!/usr/bin/env bash


echo "KMN for full"
model_dir=model_dir:full
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:10
./qpy.sh aggregate_clusters.py ${model_dir} lda:False n_groups:10

#ally: 3, 6
#echo "KMN for ally"
#model_dir=model_dir:ally
#./qpy.sh kmn_clustering.py ${model_dir} n_clusters:10
#enemy: 2, 3
#echo "KMN for enemy"
#model_dir=model_dir:enemy
#./qpy.sh kmn_clustering.py ${model_dir} n_clusters:10
#offender: 4, 6
#echo "KMN for offender"
#model_dir=model_dir:offender
#./qpy.sh kmn_clustering.py ${model_dir} n_clusters:10
