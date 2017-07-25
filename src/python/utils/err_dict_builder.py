import sys
from gensim.models import word2vec
from nltk.metrics.distance import edit_distance
import pickle
import datetime
import csv

import args_proc as args

max_edit_dist = float(args.params.get('max_edit_dist', 0.5))
min_sim = float(args.params.get('min_sim', 0.5))


# -----------------Metrics
# Generalized levenstein distance
def gld(s1, s2):
  return edit_distance(s1, s2)


# http://ieeexplore.ieee.org/document/4160958/
# Normalized Generalized levenstein distance
def ngld(s1, s2):
  alpha = 1
  dist = gld(s1, s2)
  ndist = 2 * dist / (alpha * (len(s1) + len(s2)) + dist)
  return ndist


def similar(s1, s2, max_edit_dist):
  dist = ngld(s1, s2)
  return dist < max_edit_dist


# -------------Logic
def load_w2v(w2v_filename):
  print("Loading word2vec file...")
  model = word2vec.Word2Vec.load(w2v_filename)
  model.init_sims(replace=False)
  return model


def _build_dicts(w2v_model, vocab_freq, sim_func, min_sim, max_edit_dist):
  vocab_freq_pair = sorted(vocab_freq.items(), key=lambda x: x[1], reverse=True)
  errors = dict()
  correction = dict()

  for word, freq in vocab_freq_pair:
    if word in correction.keys():
      continue

    similars = w2v_model.most_similar(word, topn=50)

    errors[word] = [w for w, s in similars if s > min_sim and sim_func(w, word, max_edit_dist)]

    if len(errors[word]) > 0:
      tuples = list(zip(errors[word], [word] * len(errors[word])))
    else:
      tuples = [(word, word)]
    c = dict(tuples)
    correction.update(c)

  return errors, correction


def save_dicts(errors, correction, err_fn, cor_fn):
  print("Saving errors .pkl file")
  with open(err_fn, 'wb') as output:
    pickle.dump(errors, output, pickle.HIGHEST_PROTOCOL)

  print("Saving corrections .pkl file")
  with open(cor_fn, 'wb') as output:
    pickle.dump(correction, output, pickle.HIGHEST_PROTOCOL)


def save_csvs(errors, correction, err_fn, cor_fn):
  with open(err_fn.replace('.pkl', '.csv'), 'w') as output:
    csvwr = csv.writer(output)
    for word, error in errors.items():
      csvwr.writerow([word, '|'.join(error) if len(error) > 0 else ''])

  with open(cor_fn.replace('.pkl', '.csv'), 'w') as output:
    csvwr = csv.writer(output)
    for word, corr in correction.items():
      csvwr.writerow([word, corr])


def build_dicts(max_edit_dist, min_sim, vocab_fn, w2v_fn, cor_fn, err_fn):
  with open(vocab_fn, "rb") as vocab_fl:
    vocab_freq = pickle.load(vocab_fl)

  print("Loading w2v model")
  w2v_model = load_w2v(w2v_fn)

  print("Looking for synonms and errors")
  errors, correction = _build_dicts(w2v_model, vocab_freq, similar, min_sim, max_edit_dist)

  save_dicts(errors, correction, err_fn, cor_fn)
  save_csvs(errors, correction, err_fn, cor_fn)


begin_time = datetime.datetime.now()

build_dicts(max_edit_dist, min_sim, args.vocab, args.w2v, args.corr, args.err)

print("Time Elapsed:", datetime.datetime.now() - begin_time)
