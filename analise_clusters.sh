#!/usr/bin/env bash


#full: 2, 3?
model_dir=full
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 sil_testing:False
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 sil_testing:False
#ally: 3, 6
model_dir=ally
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 sil_testing:False
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:6 sil_testing:False
#enemy: 2, 3
model_dir=enemy
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 sil_testing:False
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 sil_testing:False
#offender: 4, 6
model_dir=offender
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:4 sil_testing:False
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:6 sil_testing:False

#full-bigram:2, 3
model_dir=full/bigrams
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 sil_testing:False
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 sil_testing:False
#ally-bigram: 6, 9
model_dir=ally/bigrams
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:6 sil_testing:False
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:9 sil_testing:False
#enemy-bigram: 2, 3?
model_dir=enemy/bigrams
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 sil_testing:False
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 sil_testing:False
# offender-bigrams: 2,3?
model_dir=offender/bigrams
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:2 sil_testing:False
./qpy.sh kmn_clustering.py ${model_dir} n_clusters:3 sil_testing:False

