#!/usr/bin/env bash


./qpy.sh kmn_clustering.py model_dir:full sil_testing:True
./qpy.sh kmn_clustering.py model_dir:full/bigrams sil_testing:True

./qpy.sh kmn_clustering.py model_dir:ally sil_testing:True
./qpy.sh kmn_clustering.py model_dir:ally/bigrams sil_testing:True

./qpy.sh kmn_clustering.py model_dir:enemy sil_testing:True
./qpy.sh kmn_clustering.py model_dir:enemy/bigrams sil_testing:True

./qpy.sh kmn_clustering.py model_dir:offender sil_testing:True
./qpy.sh kmn_clustering.py model_dir:offender/bigrams sil_testing:True


