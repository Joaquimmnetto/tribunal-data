from pprint import pprint
import matplotlib.pyplot as plt
from gensim.models import LdaMulticore
from gensim.matutils import sparse2full
from gensim.corpora import MmCorpus
import args_proc as args
import numpy as np
import wordcloud

import group_tools


print("Loading inputs")

def save_wordclouds(weights, sufixo = ""):

	for l, v in weights:
		wc = wordcloud.WordCloud(max_font_size=250, width=500, height=500, max_words=100,
		                                        background_color='white').fit_words(v)
		sufixo = ""
		sufixo += str(l) + '_' + args.current_model
		save_wc(wc, sufixo)



def save_wc(wordcloud, sufixo):
	plt.figure()
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.savefig('wc_' + sufixo + '.png')


def main():
	topic_probs = args.params.get('topic_probs','False') == 'True'
	lda = args.params.get('lda','True') == 'True'
	nwords = int(args.params.get('nwords', 100))
	n_groups = int(args.params.get('n_groups', 4))

	if not topic_probs:
		print("Aggregating labels count")
		if lda:
			aggr_res = args.load_obj(args.aggr_lda.format(n_groups))
			labels_weight = aggr_res['labels_weight']
			groups_cont = aggr_res['groups_cont']
			topics_sum = aggr_res['topics_sum']
		else:
			aggr_res = args.load_obj(args.aggr_kmn.format(n_groups))
			labels_weight = aggr_res['labels_weight']
			groups_cont = aggr_res['groups_cont']
	else:
		print("Getting topics higest-prob. words")
		lda_model = args.load_obj(args.lda_team, gensim_class=LdaMulticore)
		labels_weight = group_tools.topic_words(lda_model, topn_words=nwords)

	print("Applying idf on top",nwords,"words")
	#[(label,[(word,weight),...])]
	lst_fwords = group_tools.groups_idf(labels_weight, num_words=nwords)

	save_wordclouds(lst_fwords,'topic_prob' if topic_probs else 'bow_sum')
	print("WordClouds saved")
	print("-------------Results----------------")
	if not topic_probs:
		print("Cluster/Topic distribution:")
		pprint(groups_cont)
		if lda:
			print("Avg. probability that a doc. belongs to a topic:")
			pprint(topics_sum)



if __name__ == '__main__':
	args.measure_time(main)