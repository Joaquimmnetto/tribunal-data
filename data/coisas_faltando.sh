#!/usr/bin/env bash

model_dir=model_dir:ally
min_freq=min_freq:800
echo "Creating the count matrix"
./qpy.sh count_matrix_builder.py ${model_dir} ${min_freq}

echo "Generating the d2v model"
./qpy.sh d2v_model_builder.py ${model_dir} ${min_freq}

echo "Generating idfs"
./qpy.sh idfs_builder.py ${model_dir}

model_dir=model_dir:enemy
min_freq=min_freq:800
echo "Creating the count matrix"
./qpy.sh count_matrix_builder.py ${model_dir} ${min_freq}

echo "Generating the d2v model"
./qpy.sh d2v_model_builder.py ${model_dir} ${min_freq}

echo "Generating idfs"
./qpy.sh idfs_builder.py ${model_dir}
