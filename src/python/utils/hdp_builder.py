import gensim
import args_proc as args
import lda_builder


def hdp_topic_discovery(corpus, id2word):
	hdp_model = gensim.models.HdpModel(corpus=corpus,id2word=id2word)
	return hdp_model


def main():
	print("Loading bow matrix:")
	gsm_corpus, id2word = lda_builder.load_cnt_matrix(args.cnt_team, args.cnt_team_vocab)
	print("Making lda model:")
	hdp_model = hdp_topic_discovery(gsm_corpus, id2word)
	hdp_model.save(args.hdp_team)
	lda_builder.save_csv(args.hdp_team_csv, hdp_model, 20, 10)
