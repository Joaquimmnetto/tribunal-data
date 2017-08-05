from gensim.models import LdaMulticore
from gensim.matutils import sparse2full
from gensim.corpora import MmCorpus
from gensim.matutils import Scipy2Corpus
from gensim.models import Doc2Vec

import sklearn.metrics.pairwise as metrics

import numpy as np
import utils

from concurrent.futures import ProcessPoolExecutor

from params import vecs,clt,args

def aggregate_kmn(bow_mat_fn, points, clusters, centers, part, vocab):  
  scipy_mat = utils.load_obj(bow_mat_fn.format(part))
  bow_mat = Scipy2Corpus(scipy_mat.tocsc())
  row = part * scipy_mat.shape[0]

  labels = sorted(list(set(clusters)))
  labels_sum = dict([(label, np.zeros(len(vocab))) for label in labels])
  topics_sum = dict([(label, np.zeros(len(labels))) for label in labels])
  topics_count = dict([(label, 0) for label in labels])
  r2l = dict()
  
  bow_r2d = utils.load_obj(vecs.bow.r2d)
  d2v_r2d = utils.load_obj(vecs.d2v.r2d)  
  
  for bow in bow_mat:    
    assert bow_r2d[row] == d2v_r2d[row]    
    lb = clusters[row]    
    r2l[row] = np.zeros(len(labels))
    r2l[row][lb] = 1
    labels_sum[lb] += sparse2full(bow, len(vocab))
    topics_sum[lb] += np.fabs(metrics.cosine_similarity(centers[lb].reshape(1,-1), points[lb].reshape(1,-1))[0,0])
    topics_count[lb] += 1
    row += 1
  del bow_mat

  return r2l, labels_sum, topics_sum, topics_count


def aggregate_lda(bow_mat_fn, lda_model, part, vocab):  
  scipy_mat = utils.load_obj(bow_mat_fn.format(part))
  bow_mat = Scipy2Corpus(scipy_mat.tocsc())    
  row = part * scipy_mat.shape[0]

  labels = range(0, lda_model.num_topics)
  labels_sum = dict([(label, np.zeros(len(vocab))) for label in labels])
  topics_sum = dict([(label, np.zeros(len(labels))) for label in labels])
  topics_count = dict([(label, 0) for label in labels])
  r2l = dict()
  
  for bow in bow_mat:      
    topics = lda_model[bow]
    first_topic = sorted(topics, key=lambda x: x[1], reverse=True)[0][0]
    #r2l[row] = first_topic
    r2l[row] = topics
    labels_sum[first_topic] += sparse2full(bow, len(vocab))
    topics_sum[first_topic] += sparse2full(topics, lda_model.num_topics)
    topics_count[first_topic] += 1
    row += 1
  del bow_mat

  return r2l, labels_sum, topics_sum, topics_count

def append_results(promise, r2l, labels_sum, topics_sum, topics_count):
  _r2l,_ls,_ts,_tc = promise.result()
  r2l.update(_r2l)
  for label in labels_sum.keys():
    labels_sum[label] += _ls[label]
    topics_sum[label] += _ts[label]
    topics_count[label] += _tc[label]
  

def summarize_topic_labels(model_name, bow_mat_fn, vocab_fn, n_workers=3):
  vocab = utils.load_obj(vocab_fn)

  if model_name=='lda':
    model = utils.load_obj(clt.lda.model, gensim_class=LdaMulticore)    
    labels = range(0, model.num_topics)
  elif model_name=='kmn':
    model = utils.load_obj(clt.kmn.labels)
    points = utils.load_obj(vecs.d2v.mtx, Doc2Vec).docvecs
    centers = utils.load_obj(clt.kmn.model)
    labels = range(0, len(centers))

  labels_sum = dict([(label, np.zeros(len(vocab))) for label in labels])
  topics_sum = dict([(label, np.zeros(len(labels))) for label in labels])
  topics_count = dict([(label, 0) for label in labels])
  r2l = dict()
  row = 0
  promises = list()
  with ProcessPoolExecutor(max_workers=n_workers) as exc:   
    for part in range(0, vecs.n_matrix):   
      if model_name=='lda':
        promise = exc.submit(aggregate_lda, bow_mat_fn, model, part, vocab)
      elif model_name=='kmn':      
        promise = exc.submit(aggregate_kmn, 
                    bow_mat_fn, points, model, centers, part, vocab)
      promises.append(promise)
    
    for promise in promises:
      append_results(promise, r2l, labels_sum, topics_sum, topics_count)

  mat_len = sum(topics_count.values())

  for label, vec in labels_sum.items():
    labels_sum[label] = sorted(list(zip(vocab, vec)), key=lambda x: x[1], reverse=True)

  for label in topics_sum.keys():
    topics_count[label] /= float(mat_len)

  return labels_sum, topics_sum, topics_count, r2l


def main():
  model = args.get("model","lda").strip()

  print("Loading labels count")
  labels_weight, topics_sum, groups_cont, r2l = summarize_topic_labels(model, vecs.bow.mtx, vecs.bow.vocab)
  res = {"model": model, "labels_weight": labels_weight, "topics_sum": topics_sum, "groups_cont": groups_cont}
  if model=='lda':
    utils.save_pkl(clt.lda.postprocess, res)
    utils.save_pkl(clt.lda.r2l, r2l)
  elif model=='kmn':
    utils.save_pkl(clt.kmn.postprocess, res)
    utils.save_pkl(clt.kmn.r2l, r2l)

if __name__ == '__main__':
  utils.measure_time(main)
