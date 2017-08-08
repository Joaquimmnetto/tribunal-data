import scipy.sparse
import scipy.io

from sklearn.feature_extraction.text import TfidfVectorizer
from doc_iterator import DocIterator
from count_matrix_builder import CountDocIterator
import count_matrix_builder

from params import args,base,vecs
import utils

min_freq = int(args.get('min_freq', 150))


def build_tfidf_matrix(chat_fn, corpus_fn):
  chat = CountDocIterator(DocIterator(chat_fn, corpus_fn))
  tfidf_model = TfidfVectorizer(min_df=min_freq, stop_words=count_matrix_builder.stwords)
  matrix = tfidf_model.fit_transform(chat)

  return chat.row_doc, tfidf_model.get_feature_names(), matrix


def main():
  print("Building tf-idf matrix")
  docs, vocab, tfidf_matrix = build_tfidf_matrix(base.chat, base.corpus)
  print("Saving models...")
  #TODO refatorar isso
  count_matrix_builder.save_outp(row_doc=docs, row_doc_fn=vecs.tfidf.r2d,
                                 vocab=vocab, vocab_fn=vecs.tfidf.vocab,
                                 matrix=None, matrix_fn=None)
  #TODO dividir essa matriz.
  # scipy.io.mmwrite(args.tfidf_team, tfidf_matrix, field='real', precision=4)


if __name__ == '__main__':
  utils.measure_time(main)
