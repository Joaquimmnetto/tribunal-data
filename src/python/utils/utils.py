import datetime
import pickle
import scipy.io
import math
import csv


def measure_time(main):
  before = datetime.datetime.now()
  main()
  print("Time elapsed:", datetime.datetime.now() - before)


def save_pkl(fname, obj):
  pickle.dump(obj, open(fname, 'wb'), protocol=2, fix_imports=True)


def load_obj(fname, gensim_class=None):
  if fname.endswith('.pkl'):
    return pickle.load(open(fname, 'rb'))
  if fname.endswith('.mtx') or fname.endswith('.mm'):
    return scipy.io.mmread(fname)
  if fname.endswith('.gsm') or fname.endswith('.bin'):
    return gensim_class.load(fname)


def load_spy_matrix(data_fn, vocab):
  id2word = load_obj(vocab)
  id2word = dict([(i, v) for i, v in enumerate(id2word)])

  corpus = load_obj(data_fn)
  return corpus, id2word


def topic_words(topic_model, topn_topics=-1, topn_words=100):
  topics = topic_model.show_topics(num_topics=topn_topics, num_words=topn_words, formatted=False)
  return dict(topics)


def groups_tfidf(groups, dfs, num_words=100):
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
    # result = [(n, ws[0:num_words]) for n, ws in result]

  return result


def save_csv(topic_team_csv, topics):
  csv_wr = csv.writer(open(topic_team_csv, 'w'))
  for topic in topics:
    i = topic[0]
    for w, p in topic[1]:
      csv_wr.writerow([i, w, p])
