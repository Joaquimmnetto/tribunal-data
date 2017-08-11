echo "LDA single-thread"
./qpy.sh lda_builder.py base_dir:base model_dir:model_drift_auto num_topics:15 mt:False

#echo "Post-process"
#./qpy.sh aggregate_clusters.py base_dir:base model_dir:model_drift model:lda n_workers:3

#echo "Generate vizualisations"
#./qpy.sh prepare_ldavis.py base_dir:base model_dir:model_drift n_workers:3

echo "Finished!"
