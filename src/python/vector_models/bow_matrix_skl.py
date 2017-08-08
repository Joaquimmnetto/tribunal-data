import scipy.sparse
import scipy.io
from six import iteritems

from params import args, vecs, base
from utils import utils

from bow_iterator import CountDocIterator

from gensim.corpora import Dictionary
from doc_iterator import DocIterator
from sklearn.feature_extraction.text import CountVectorizer


min_freq = int(args.get('min_freq', 800))
timeslice = int(args.get('timeslice', 600))
champs_fn = args.get("champs", 'base/champs.txt')
stwords_fn = args.get("stwords", 'base/en_stopwords.txt')


champs = [champ.strip('\n').strip(' ').lower() for champ in open(champs_fn)]
stwords = [sw.strip('\n').strip(' ').lower() for sw in open(stwords_fn)] + champs


def build_bow_matrix(chat_fn, corpus_fn, _timeslice = timeslice, _min_freq=min_freq, vocab=None):
  chat = CountDocIterator(DocIterator(chat_fn, corpus_fn, _timeslice), False)

  cnt_model = CountVectorizer(min_df=_min_freq, stop_words=stwords, vocabulary=vocab)
  matrix = cnt_model.fit_transform(chat)
  cnt_vocab = cnt_model.get_feature_names()
  
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
  print("Building counting matrix")
  docs, cnt_vocab, cnt_matrix = build_bow_matrix(base.chat, base.corpus, timeslice)
  print(cnt_matrix.shape[0])

  print("Saving models...")
  save_outp(docs, vecs.bow.r2d,
            cnt_vocab, vecs.bow.vocab,
            cnt_matrix, vecs.bow.mtx)


# print("Total time elapsed:", datetime.datetime.now() - before)


if __name__ == '__main__':
  utils.measure_time(main)
