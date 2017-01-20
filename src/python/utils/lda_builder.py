import csv
import datetime
import pickle
import scipy.io
import gensim.matutils
from gensim.models import LdaMulticore

import args_proc as args

num_topics = int(args.params.get("num_topics",10))


def load_cnt_matrix(data_fn, vocab):
	id2word = pickle.load(open(vocab, 'rb'))
	id2word = dict([(i, v) for i, v in enumerate(id2word)])

	bow_matrix = scipy.io.mmread(data_fn)
	print(bow_matrix.shape)
	corpus = gensim.matutils.Scipy2Corpus(bow_matrix.tocsc())

	return corpus, id2word


def load_spy_matrix(data_fn, vocab):
	id2word = pickle.load(open(vocab, 'rb'))
	id2word = dict([(i, v) for i, v in enumerate(id2word)])

	corpus = gensim.corpora.MmCorpus(data_fn)

	return corpus, id2word



def lda_topic_discovery(corpus, id2word, num_topics):
	lda_model = LdaMulticore(corpus=corpus, num_topics=num_topics, id2word=id2word, workers=3)
	return lda_model


def save_csv(lda_team_csv, lda_model, topn_topics=-1, topn_words=10):
	csv_wr = csv.writer(open(lda_team_csv,'w'))
	topics = sorted(lda_model.show_topics(num_topics=topn_topics, num_words=topn_words, formatted=False),
	                key=lambda v: v[1], reverse=True)
	for topic in topics: #topic=( num,[words] )
		i = topic[0]
		for w,p in topic[1]:
			csv_wr.writerow([i, w, p])




def main():
	before = datetime.datetime.now()
	print("Loading bow matrix:")
	gsm_corpus, id2word = load_cnt_matrix(args.cnt_team, args.cnt_team_vocab)
	print("Making lda model:")
	lda_model = lda_topic_discovery(gsm_corpus, id2word, num_topics)
	lda_model.save(args.lda_team)
	save_csv(args.lda_team_csv,lda_model,20,10)

	print("Time elapsed:", datetime.datetime.now() - before)


if __name__ == '__main__':
	main()
