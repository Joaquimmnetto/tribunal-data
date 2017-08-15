import scipy.sparse
import scipy.io
import numpy as np
from six import iteritems
from calculate_df import process_df
import params
from params import args, vecs, base
import utils

from gensim.corpora import Dictionary
from doc_iterator import DocIterator
from sklearn.feature_extraction.text import CountVectorizer


min_freq = int(args.get('min_freq', 800))
timeslice = int(args.get('timeslice', 600))
champs_fn = args.get("champs", params.data_dir+'base/champs.txt')
stwords_fn = args.get("stwords", params.data_dir+'base/en_stopwords.txt')


champs = [champ.strip('\n').strip(' ').lower() for champ in open(champs_fn)]
stwords = [sw.strip('\n').strip(' ').lower() for sw in open(stwords_fn)] + champs
# with open(args.words, 'rb') as inp:
#   vocab_words = pickle.load(inp)



# vocab_words = [word for word in vocab_words if word not in stwords]


class CountDocIterator(object):
  def __init__(self, doc_iter, gensim=False):
    self.docs_iter = doc_iter
    self.row_doc = dict()
    self.gensim = gensim

  def __iter__(self):
    stop = False
    index = 0
    for case, match, team, docs in self.docs_iter.next_doc():
      for timeslice, doc in enumerate(docs):
        if doc.strip('\n').strip('\t').strip('\r').strip(' ') == '':
          continue
        self.row_doc[index] = (case, match, team, timeslice)
        index += 1
        if not self.gensim:
          yield doc
        else:
          yield doc.split()


def build_cnt_matrix(chat_fn, corpus_fn, _timeslice = timeslice, _min_freq=min_freq, vocab=None, gensim=False):
  chat = CountDocIterator(DocIterator(chat_fn, corpus_fn, _timeslice), gensim)
  if not gensim:
    cnt_model = CountVectorizer(min_df=_min_freq, stop_words=stwords, vocabulary=vocab)
    matrix = cnt_model.fit_transform(chat)
    cnt_vocab = cnt_model.get_feature_names()

  else:
    matrix = Dictionary(chat)
    stop_ids = [matrix.token2id[sword] for sword in stwords
                if sword in matrix.token2id]
    unfreq_ids = [tokenid for tokenid, docfreq in iteritems(matrix.dfs) if docfreq < min_freq]
    matrix.filter_tokens(stop_ids + unfreq_ids)
    cnt_vocab = matrix.token2id

  return chat.row_doc, cnt_vocab, matrix


def save_outp(row_doc, row_doc_fn, vocab, vocab_fn, matrix, matrix_fn):
  if row_doc is not None:
    utils.save_pkl(row_doc_fn,row_doc)

  if vocab is not None:
    utils.save_pkl(vocab_fn, vocab)

  if matrix is not None:
    n = vecs.n_matrix
    for i in range(0, n):
      with open(matrix_fn.format(i), 'wb') as output:
        print("Saving matrix ", i)
        scipy.io.mmwrite(output, matrix[i * int(matrix.shape[0] / n): (i + 1) * int(matrix.shape[0] / n), :])


def main():
  freq = None
  print("Building counting matrix")
  docs, cnt_vocab, cnt_matrix = build_cnt_matrix(base.chat, base.corpus, timeslice)
      
  freq = cnt_matrix.sum(axis=0)   
  freq = np.array(freq)[0] 

  utils.save_pkl(vecs.df, freq)

  print("Saving models...")
  save_outp(docs, vecs.bow.r2d,
            cnt_vocab, vecs.bow.vocab,
            cnt_matrix, vecs.bow.mtx)            


# print("Total time elapsed:", datetime.datetime.now() - before)


if __name__ == '__main__':
  utils.measure_time(main)
