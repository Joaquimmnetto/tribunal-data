import args_proc as args
import gensim
import group_tools


num_topics = int(args.params.get("num_topics",300))


def lsi_topic_discovery(corpus,id2word,ntopics):
	lsi_model = gensim.models.LsiModel(corpus=corpus,num_topics=ntopics,id2word=id2word)
	lsi_matrix = lsi_model[corpus]
	return lsi_model, lsi_matrix


def main():
	print("Skipping LSI, too heavy!")
	# print("Loading inputs...")
	# tfidf_corpus, tfidf_id2word = topic_tools.load_spy_matrix(args.tfidf_team, args.tfidf_team_vocab)
	# print("Applying LSI model...")
	# lsi_model, lsi_mat = lsi_topic_discovery(tfidf_corpus,tfidf_id2word, ntopics=num_topics)
	#
	# print("Saving results...")
	# lsi_model.save(args.lsi_team_model)
	# gensim.corpora.MmCorpus.serialize(args.lsi_team_matrix, lsi_mat)


if __name__ == '__main__':
	args.measure_time(main)

