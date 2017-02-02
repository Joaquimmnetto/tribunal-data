#!/usr/bin/env bash
#
##full: 2, 3? (5)
##full-bigram:2, 3
#
##ally: 3, 6(4)
##ally-bigram: 6, 9
#
##enemy: 2, 3(3)
##enemy-bigram: 2, 3?
#
##offender: 4, 6(5)
## offender-bigrams: 2,3?
#
#ntopics_full=5
#ntopics_ally=10
#ntopics_enemy=10
#ntopics_offender=10
#
#echo "LDA for full:"
#model_dir=model_dir:full
#out_dir=analise
#ntopics=${ntopics_full}
#lda_team=lda_team:${out_dir}/lda_full_${n_topics}.gsm
#echo "LDA for full and ${ntopics} topics"
#./qpy.sh lda_builder.py ${model_dir} num_topics:${ntopics} ${lda_team} lda_team_csv:${out_dir}/lda_full_${ntopics}.csv
#./qpy.sh aggregate_clusters.py ${model_dir} ${lda_team} n_groups:${ntopics} lda:True
#./qpy.sh cluster_analysis.py ${model_dir} n_groups:${ntopics} topic_probs:False lda:True nwords:100 > lda_full_${ntopics}.txt
#
#echo "LDA for ally:"
#model_dir=model_dir:ally
#out_dir=analise
#ntopics=${ntopics_ally}
#lda_team=lda_team:${out_dir}/lda_ally_${ntopics}.gsm
#echo "LDA for ally and ${ntopics} topics"
#./qpy.sh lda_builder.py ${model_dir} num_topics:${ntopics} ${lda_team} lda_team_csv:${out_dir}/lda_ally_${ntopics}.csv
#./qpy.sh aggregate_clusters.py ${model_dir} ${lda_team} n_groups:${ntopics} lda:True
#./qpy.sh cluster_analysis.py ${model_dir} n_groups:${ntopics} topic_probs:False lda:True nwords:100 > lda_ally_${ntopics}.txt
#
#echo "LDA for enemy:"
#model_dir=model_dir:enemy
#out_dir=analise
#ntopics=${ntopics_enemy}
#lda_team=lda_team:${out_dir}/lda_enemy_${ntopics}.gsm
#
#echo "LDA for enemy and ${ntopics} topics"
#./qpy.sh lda_builder.py ${model_dir} num_topics:${ntopics} ${lda_team} lda_team_csv:${out_dir}/lda_enemy_${ntopics}.csv
#./qpy.sh aggregate_clusters.py ${model_dir} ${lda_team} n_groups:${ntopics} lda:True
#./qpy.sh cluster_analysis.py ${model_dir} n_groups:${ntopics} topic_probs:False lda:True nwords:100 > lda_enemy_${ntopics}.txt
#
#echo "LDA for offender:"
#model_dir=model_dir:offender
#out_dir=analise
#ntopics=${ntopics_offender}
#lda_team=lda_team:${out_dir}/lda_offender_${ntopics}.gsm
#echo "LDA for offender and ${ntopics} topics"
#./qpy.sh lda_builder.py ${model_dir} num_topics:${ntopics} ${lda_team} lda_team_csv:${out_dir}/lda_offender_${ntopics}.csv
#./qpy.sh aggregate_clusters.py ${model_dir} ${lda_team} n_groups:${ntopics} lda:True
#./qpy.sh cluster_analysis.py ${model_dir} n_groups:${ntopics} topic_probs:False lda:True nwords:100 > lda_offender_${ntopics}.txt
