import gensim
from pprint import pprint
import args_proc as args
import group_tools


def hdp_topic_discovery(corpus, id2word):
  hdp_model = gensim.models.HdpModel(corpus=corpus, id2word=id2word)
  return hdp_model


def main():
  print("Loading bow matrix:")
  gsm_corpus, id2word = group_tools.load_spy_matrix(args.cnt_team, args.cnt_team_vocab)
  print("Making HDA model:")
  hdp_model = hdp_topic_discovery(gsm_corpus, id2word)
  print("Saving results")
  hdp_model.save(args.hdp_team)

  topics = group_tools.groups_idf(hdp_model)
  pprint(topics)
  group_tools.save_csv(args.hdp_team_csv, topics)
  pprint(len(topics))

# if __name__ == '__main__':
#	args.measure_time(main)
