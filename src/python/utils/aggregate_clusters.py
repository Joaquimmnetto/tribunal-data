from gensim.models import LdaMulticore
from gensim.matutils import sparse2full
from gensim.corpora import MmCorpus
from gensim.matutils import Scipy2Corpus
import numpy as np
import utils
from params import vecs,clt


def summarize_topic_labels(bow_mat_fn, vocab_fn, lda_fn):
  vocab = utils.load_obj(vocab_fn)
  lda_model = utils.load_obj(lda_fn, gensim_class=LdaMulticore)

  labels = range(0, lda_model.num_topics)
  labels_sum = dict([(label, np.zeros(len(vocab))) for label in labels])
  topics_sum = dict([(label, np.zeros(len(labels))) for label in labels])
  topics_count = dict([(label, 0) for label in labels])
  r2l = dict()
  row = 0

  for part in range(0, vecs.n_matrix):
    scipy_mat = utils.load_obj(bow_mat_fn.format(part))
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
  vocab = utils.load_obj(vocab_fn)

  labels = utils.load_obj(clt.kmn.format(n_clusters))

  which_labels, counts = np.unique(labels, return_counts=True)

  labels_sum = dict([(label, len(vocab)) for label in which_labels])
  for i, bow in enumerate(bow_mat):
    labels_sum[labels[i]] += sparse2full(bow, len(vocab))
  del bow_mat

  for label, vec in labels_sum.items():
    labels_sum[label] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)

  return labels_sum, counts


def main():
  print("Loading labels count")
  labels_weight, topics_sum, groups_cont, r2l = summarize_topic_labels(vecs.bow.mtx, vecs.bow.vocab, clt.lda.model)
  res = {"lda": True, "labels_weight": labels_weight, "topics_sum": topics_sum, "groups_cont": groups_cont}

  utils.save_pkl(clt.lda.postprocess, res)
  utils.save_pkl(clt.lda.r2l, r2l)

if __name__ == '__main__':
  utils.measure_time(main)
