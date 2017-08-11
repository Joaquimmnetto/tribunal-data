echo "LDA"
./qpy.sh lda_builder.py base_dir:base model_dir:model_drift num_topics:8 model:lda

echo "Post-process"
./qpy.sh aggregate_clusters.py base_dir:base model_dir:model_drift model:lda n_workers:3

echo "Generate vizualisations"
./qpy.sh prepare_ldavis.py base_dir:base model_dir:model_drift n_workers:3

echo "Finished!"
