import args_proc as args
import math
import csv

import gensim


def load_spy_matrix(data_fn, vocab):
	id2word = args.load_obj(vocab)
	id2word = dict([(i, v) for i, v in enumerate(id2word)])

	corpus = gensim.corpora.MmCorpus(data_fn)
	return corpus, id2word


def topic_words(topic_model, topn_topics=-1, topn_words=100):
	topics = topic_model.show_topics(num_topics=topn_topics, num_words=topn_words, formatted=False)
	return dict(topics)

def groups_idf(groups, num_words=100):
	idfs = args.load_obj(args.idf_team)
	result = []

	for num,words in groups.items():
		new_words = []
		for w,p in words[:num_words]:
			if p == 0:
				idfp = -math.inf
			else:
				idfp = math.log2(p * idfs[w])
			new_words.append((w,idfp))
		result.append((num, sorted(new_words, key=lambda v: v[1], reverse=True)) )

	#result = [(n, ws[0:num_words]) for n, ws in result]

	return result


def save_csv(topic_team_csv, topics):
	csv_wr = csv.writer(open(topic_team_csv, 'w'))
	for topic in topics:
		i = topic[0]
		for w,p in topic[1]:
			csv_wr.writerow([i, w, p])