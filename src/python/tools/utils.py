import datetime
import pickle
import math
import csv

import scipy.io
import scipy.sparse
from gensim.corpora import MmCorpus


class GensimCorpus:
  def __init__(self, gsm_dict, corpus):
    self.gsm_dict = gsm_dict
    self.corpus = corpus

  def __iter__(self):
    for doc in self.corpus:
      yield self.gsm_dict.doc2bow(doc)

def measure_time(main):
  before = datetime.datetime.now()
  main()
  print("Time elapsed:", datetime.datetime.now() - before)


def save(fname, obj, nparts=1):
  if nparts > 1:
    print("Total size:", obj.shape[0])
    print("Part size:", int(obj.shape[0] / nparts))
    for i in range(0, nparts):    
      print("Saving matrix ", i)      
      if scipy.sparse.issparse(obj): 
        scipy.io.mmwrite(fname.format(i), obj[i * int(obj.shape[0] / nparts): (i + 1) * int(obj.shape[0] / nparts), :])         
    return

  elif fname.endswith('.pkl'):
    pickle.dump(obj, open(fname, 'wb'), protocol=2, fix_imports=True)
  elif fname.endswith('.mtx') or fname.endswith('.mm'):    
    if scipy.sparse.issparse(obj): 
      scipy.io.mmwrite(fname, obj)
    elif isinstance(obj, GensimCorpus):
       MmCorpus.serialize(fname, corpus = obj)

  elif fname.endswith('.gsm') or fname.endswith('.bin'):
      obj.save(fname)
    
def load(fname, gensim_class=None):
  if fname.endswith('.pkl'):
    return pickle.load(open(fname, 'rb'))
  if fname.endswith('.mtx') or fname.endswith('.mm'):
    return scipy.io.mmread(fname)
  if fname.endswith('.gsm') or fname.endswith('.bin'):
    return gensim_class.load(fname)


def topic_words(topic_model, topn_topics=-1, topn_words=100):
  topics = topic_model.show_topics(num_topics=topn_topics, num_words=topn_words, formatted=False)
  return dict(topics)


def groups_tfidf(groups, vocab, dfs, num_words=100):
  dfs = dict(zip(vocab, dfs))
  result = []
  for num, words in groups.items():
    new_words = []
    for w, p in words[:num_words]:
      if p == 0 or (w not in dfs.keys()) or dfs[w] == 0:
        idfp = -math.inf
      else:
        idfp = math.log(p * (1.0 / float(dfs[w])))
      new_words.append((w, idfp))
    result.append((num, sorted(new_words, key=lambda v: v[1], reverse=True)))

  return result


def save_csv(topic_team_csv, topics):
  csv_wr = csv.writer(open(topic_team_csv, 'w'))
  for topic in topics:
    i = topic[0]
    for w, p in topic[1]:
      csv_wr.writerow([i, w, p])
