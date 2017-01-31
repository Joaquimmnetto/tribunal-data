
import datetime
from pprint import pprint
from gensim.models import LdaMulticore
import group_tools
import args_proc as args

num_topics = int(args.params.get("num_topics", 4))
analysis = bool(args.params.get("analysis", False))


def lda_topic_discovery(corpus, id2word, num_topics):
	lda_model = LdaMulticore(corpus=corpus, num_topics=num_topics, id2word=id2word, workers=5)
	return lda_model



#Multiplicar as probabilidade das palavras pelo idf delas, após ter o modelo pronto, para auxiliar na interpretação(livro cap.6).
def main():
	if not analysis:
		print("Loading bow matrix:")
		gsm_corpus, id2word = group_tools.load_spy_matrix(args.cnt_team, args.cnt_team_vocab)
		print("Making lda model:")
		lda_model = lda_topic_discovery(gsm_corpus, id2word, num_topics)
		lda_model.save(args.lda_team)
	else:
		lda_model = LdaMulticore.load(args.lda_team)

	topics_sum = group_tools.topic_words(lda_model, topn_words=100)
	topics = group_tools.groups_idf(topics_sum)
	if analysis:
		pprint(topics)
	group_tools.save_csv(args.lda_team_csv, topics)



if __name__ == '__main__':
	args.measure_time(main)
