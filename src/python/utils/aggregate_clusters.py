from gensim.models import LdaMulticore
from gensim.matutils import sparse2full
from gensim.corpora import MmCorpus
from gensim.matutils import Scipy2Corpus
import numpy as np
import args_proc as args
import csv


def summarize_topic_labels(bow_mat_fn, vocab_fn, lda_fn):
  vocab = args.load_obj(vocab_fn)
  lda_model = args.load_obj(lda_fn, gensim_class=LdaMulticore)

  labels = range(0, lda_model.num_topics)
  labels_sum = dict([(label, np.zeros(len(vocab))) for label in labels])
  topics_sum = dict([(label, np.zeros(len(labels))) for label in labels])
  topics_count = dict([(label, 0) for label in labels])
  r2l = dict()
  row = 0

  for part in range(0, args.n_matrixes):
    scipy_mat = args.load_obj(bow_mat_fn.format(part))   
    bow_mat = Scipy2Corpus(scipy_mat.tocsc())
    for bow in bow_mat:
      topics = lda_model[bow]
      first_topic = sorted(topics, key=lambda x: x[1], reverse=True)[0][0]
      r2l[row] = first_topic
      labels_sum[first_topic] += sparse2full(bow, len(vocab))
      topics_sum[first_topic] += sparse2full(topics, lda_model.num_topics)
      topics_count[first_topic] += 1
      row += 1
    del bow_mat

  mat_len = sum(topics_count.values())

  for label, vec in labels_sum.items():
    labels_sum[label] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)

  for label in topics_sum.keys():
    topics_count[label] /= float(mat_len)

  return labels_sum, topics_sum, topics_count, r2l


def summarize_labels(bow_mat, lda_model, vocab):
  labels = range(0, lda_model.num_topics)
  labels_sum = dict([(label, np.zeros(len(vocab))) for label in labels])
  topics_sum = dict([(label, np.zeros(len(labels))) for label in labels])
  topics_count = dict([(label, 0) for label in labels])
  r2l = dict()
  row = 0

  for bow in bow_mat:
    topics = lda_model[bow]
    first_topic = sorted(topics, key=lambda x: x[1], reverse=True)[0][0]
    r2l[row] = first_topic

    labels_sum[first_topic] += sparse2full(bow, len(vocab))
    topics_sum[first_topic] += sparse2full(topics, lda_model.num_topics)
    topics_count[first_topic] += 1
    row += 1

  mat_len = sum(topics_count.values())

  for label, vec in labels_sum.items():
    labels_sum[label] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)

  for label in topics_sum.keys():
    topics_count[label] /= float(mat_len)

  return labels_sum, topics_sum, topics_count, r2l


def summarize_cluster_labels(bow_mat_fn, n_clusters, vocab_fn):
  bow_mat = MmCorpus(bow_mat_fn)
  vocab = args.load_obj(vocab_fn)

  labels = args.load_obj(args.kmn_team_labels.format(n_clusters))

  which_labels, counts = np.unique(labels, return_counts=True)

  labels_sum = dict([(label, len(vocab)) for label in which_labels])
  for i, bow in enumerate(bow_mat):
    labels_sum[labels[i]] += sparse2full(bow, len(vocab))
  del bow_mat

  for label, vec in labels_sum.items():
    labels_sum[label] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)

  return labels_sum, counts


def main():
  lda = args.params.get('lda', 'True') == 'True'
  n_groups = 15

  print("Loading labels count")
  if lda:
    labels_weight, topics_sum, groups_cont, r2l = summarize_topic_labels(args.cnt_team, args.cnt_team_vocab, args.lda_team)
    res = {"lda": True, "labels_weight": labels_weight, "topics_sum": topics_sum, "groups_cont": groups_cont}
    args.save_pkl(args.aggr_lda_time, res)
    args.save_pkl(args.lda_time_labels, r2l)
  else:
    labels_weight, groups_cont = summarize_cluster_labels(args.cnt_team, n_groups, args.cnt_team_vocab)
    res = {"lda": False, "labels_weight": labels_weight, "groups_cont": groups_cont}
    args.save_pkl(args.aggr_kmn.format(n_groups), res)


if __name__ == '__main__':
  args.measure_time(main)
