import args_proc as args
import count_matrix_builder as bow_builder
import aggregate_clusters as summarize
import lda_builder
import group_tools
import numpy as np
from gensim.matutils import Scipy2Corpus
from pprint import pprint

ntop_words = args.params.get('ntop_words', 100)
num_topics = args.params.get('num_topics', 10)
build_models = args.params.get('build_models', True)
timeslice_size = int(args.params.get('timeslice_size', 600))
top_x = int(args.params.get('top_x', 10))
base_model = args.params.get('base_model', 'team')
matrix_from_file = args.params.get('mtx_file', False)

if base_model == 'team':
  cnt_r2d = args.cnt_team_r2d
  lda_model_fn = args.lda_team
  lda_labels = args.lda_team_labels
  aggr_lda = args.aggr_lda_teams
else:
  cnt_r2d = args.cnt_time_r2d
  lda_model_fn = args.lda_time
  lda_labels = args.lda_time_labels
  aggr_lda = args.aggr_lda_time


def main():
  if build_models:
    print('Using model:',base_model)
    print("Building bow matrix")
    row2doc, bow_vocab, bow_matrix = bow_builder.build_cnt_matrix(args.chat_parsed,
                                                                  args.corpus,
                                                                  _min_freq=800,
                                                                  _timeslice=timeslice_size)

    model_drift = "model_drift/"
    bow_builder.save_outp(row2doc,model_drift+"row2doc_2.pkl",
                         bow_vocab,model_drift+"bow_vocab_2.pkl",
                         bow_matrix, model_drift+"bow_drift_2_{0}.mm")
    return

    print("Calculating df")
    df = build_df(bow_matrix, bow_vocab)

    print("Building lda model")
    id2word = dict([(i, v) for i, v in enumerate(bow_vocab)])
    gsm_corpus = Scipy2Corpus(bow_matrix)
    lda_model = lda_builder.lda_topic_discovery(gsm_corpus, id2word, num_topics)

    print("Labeling documents and summarizing labels")
    topics_words, topics_sum, topics_count, row2lab = summarize.summarize_labels(gsm_corpus, lda_model, bow_vocab)

    print("Salvando os resultados encontrados...")
    lda_model.save(lda_model_fn)
    args.save_pkl(lda_labels, row2lab)
    args.save_pkl(cnt_r2d, row2doc)
    args.save_pkl(args.idf, df)
    args.save_pkl(aggr_lda, dict({'topics_words': topics_words,
                                  'topics_sum': topics_sum,
                                  'topics_count': topics_count})
                  )
  else:
    print("Loading Results:")
    aggr_results = args.load_obj(aggr_lda)
    topics_words = aggr_results['topics_words']
    topics_sum = aggr_results['topics_sum']
    topics_count = aggr_results['topics_count']
    print("Loading document frequency")
    df = args.load_obj(args.idf)

  print("Printing the analysis results... ")
  analyze_clusters(topics_words, topics_sum, topics_count, df)


def build_df(bow_matrix, bow_vocab):
  df_values = bow_matrix.sum(axis=0)
  df = dict([(w, c) for w, c in zip(bow_vocab, df_values.A1)])
  return df


def analyze_clusters(topics_words, topics_sum, topics_count, df):
  lst_fwords = group_tools.groups_tfidf(topics_words, df, num_words=ntop_words)

  print("-----------------Results----------------------")
  print("")
  print("Top", top_x, "words for each cluster")

  for gr_lst in lst_fwords:
    print("Cluster", gr_lst[0])
    print([(word, "%.2f" % w) for word, w in gr_lst[1][:top_x]])
  print("Cluster/Topic distribution")
  pprint(topics_count)

  print("Avg. probability that a doc belongs to a topic")
  for topic in topics_sum.keys():
    total = np.sum(topics_sum[topic])
    topics_sum[topic] *= (100 / total)
  pprint(topics_sum)


if __name__ == '__main__':
  args.measure_time(main)
